/**
 * Agent RAG API 客户端
 *
 * 知识库管理 + 文档上传 + RAG 对话（含 SSE 流式）
 */

import api from '../index'

// ============ 类型定义 ============

export interface KnowledgeBase {
  id: number
  name: string
  description?: string
  embedding_model: string
  status: boolean
  document_count: number
  chunk_count: number
  created_at: string
  updated_at: string
}

export interface KBStats {
  kb_id: number
  name: string
  document_count: number
  chunk_count: number
  indexed_chunks: number
  indexed_docs: number
}

export interface Document {
  id: number
  kb_id: number
  title: string
  content: string
  source?: string
  doc_type: string
  chunk_count: number
  status: boolean
  created_at: string
  updated_at: string
}

export interface Conversation {
  id: number
  user_id: number
  kb_id?: number
  title: string
  created_at: string
  updated_at: string
  messages: Message[]
}

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  sources?: string[]
  created_at: string
}

export interface ChatResponse {
  conversation_id: number
  answer: string
  sources: string[]
  retrieved_chunks: number
}

// ============ API 方法 ============

export const ragApi = {
  // ---- 知识库 ----
  getKnowledgeBases: () => api.get<any, KnowledgeBase[]>('/rag/knowledge-bases'),

  createKnowledgeBase: (data: { name: string; description?: string }) =>
    api.post<any, KnowledgeBase>('/rag/knowledge-bases', data),

  getKnowledgeBase: (id: number) =>
    api.get<any, KnowledgeBase>(`/rag/knowledge-bases/${id}`),

  updateKnowledgeBase: (id: number, data: { name?: string; description?: string; status?: boolean }) =>
    api.put<any, KnowledgeBase>(`/rag/knowledge-bases/${id}`, data),

  deleteKnowledgeBase: (id: number) =>
    api.delete(`/rag/knowledge-bases/${id}`),

  getKBStats: (id: number) =>
    api.get<any, KBStats>(`/rag/knowledge-bases/${id}/stats`),

  // ---- 文档 ----
  getDocuments: (kbId: number) =>
    api.get<any, Document[]>(`/rag/knowledge-bases/${kbId}/documents`),

  createDocument: (kbId: number, data: { title: string; content: string; source?: string }) =>
    api.post<any, Document>(`/rag/knowledge-bases/${kbId}/documents`, data),

  uploadDocument: (kbId: number, file: File, useLlmSplit: boolean = true) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('use_llm_split', String(useLlmSplit))
    return api.post<any, { message: string; document: Document; chunks: number; indexed: number }>(
      `/rag/knowledge-bases/${kbId}/upload`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' }, timeout: 120000 },
    )
  },

  deleteDocument: (docId: number) =>
    api.delete(`/rag/documents/${docId}`),

  getDocumentChunks: (docId: number) =>
    api.get<any, { doc_id: number; doc_title: string; total: number; chunks: { id: number; chunk_index: number; content: string; char_count: number }[] }>(
      `/rag/documents/${docId}/chunks`
    ),

  reindexDocument: (docId: number) =>
    api.post<any, { message: string; indexed: number }>(`/rag/documents/${docId}/reindex`),

  // ---- 对话 ----
  chat: (data: { message: string; kb_id?: number; conversation_id?: number }) =>
    api.post<any, ChatResponse>('/rag/chat', data, { timeout: 120000 }),

  getConversations: (kbId?: number) =>
    api.get<any, Conversation[]>('/rag/conversations', { params: kbId ? { kb_id: kbId } : {} }),

  getConversation: (id: number) =>
    api.get<any, Conversation>(`/rag/conversations/${id}`),

  deleteConversation: (id: number) =>
    api.delete(`/rag/conversations/${id}`),

  /**
   * SSE 流式对话
   *
   * 事件协议：
   * - [RETRIEVING]         — 正在检索知识库
   * - [CONTEXT]{json}      — 检索结果摘要 {count, sources}
   * - 普通文本              — AI 回复流式输出
   * - [DONE]{json}         — 完成 {conversation_id, sources, retrieved_chunks}
   * - [ERROR]msg           — 错误
   */
  async chatStream(
    data: { message: string; kb_id?: number; conversation_id?: number },
    callbacks: {
      onRetrieving?: () => void
      onContext?: (info: { count: number; sources: string[] }) => void
      onChunk?: (text: string) => void
      onDone?: (info: { conversation_id: number; sources: string[]; retrieved_chunks: number }) => void
      onError?: (error: string) => void
    },
  ): Promise<void> {
    const token = localStorage.getItem('token') || ''
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''

    try {
      const response = await fetch(`${baseURL}/api/rag/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        const errText = await response.text()
        callbacks.onError?.(`请求失败 (${response.status}): ${errText}`)
        return
      }

      const reader = response.body?.getReader()
      if (!reader) {
        callbacks.onError?.('无法获取响应流')
        return
      }

      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const payload = line.slice(6)

          if (payload === '[RETRIEVING]') {
            callbacks.onRetrieving?.()
            continue
          }

          if (payload.startsWith('[CONTEXT]')) {
            try {
              const info = JSON.parse(payload.slice('[CONTEXT]'.length))
              callbacks.onContext?.(info)
            } catch { /* ignore */ }
            continue
          }

          if (payload.startsWith('[DONE]')) {
            try {
              const info = JSON.parse(payload.slice('[DONE]'.length))
              callbacks.onDone?.(info)
            } catch {
              callbacks.onDone?.({ conversation_id: 0, sources: [], retrieved_chunks: 0 })
            }
            return
          }

          if (payload.startsWith('[ERROR]')) {
            callbacks.onError?.(payload.slice('[ERROR]'.length))
            return
          }

          // 普通文本 — AI 回复
          callbacks.onChunk?.(payload.replace(/\\n/g, '\n'))
        }
      }

      callbacks.onDone?.({ conversation_id: 0, sources: [], retrieved_chunks: 0 })
    } catch (err: any) {
      callbacks.onError?.(err?.message || '网络请求失败')
    }
  },
}
