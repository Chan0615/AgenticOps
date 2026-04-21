/**
 * 系统 AI 助手 API 客户端
 *
 * 对应后端路由：/api/assistant/*
 * 支持 tool-calling、SSE 流式输出、写操作确认
 */

import api from './index'

// ============ 类型定义 ============

export interface AssistantConversation {
  id: number
  title: string
  created_at: string
  updated_at: string
}

export interface AssistantMessage {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  sources?: string[] | null
  created_at?: string
}

export interface AssistantConversationDetail extends AssistantConversation {
  messages: AssistantMessage[]
}

export interface PendingAction {
  tool_name: string
  tool_args: Record<string, any>
  description: string
  conversation_id?: number
}

export interface AssistantChatResponse {
  conversation_id: number
  answer: string
  pending_action: PendingAction | null
  sources: string[]
}

export interface AssistantConfirmResponse {
  conversation_id: number
  answer: string
  success: boolean
}

// ============ API 方法 ============

export const assistantApi = {
  /** 非流式对话 */
  chat: (data: { message: string; conversation_id?: number }) =>
    api.post<any, AssistantChatResponse>('/assistant/chat', data, { timeout: 120000 }),

  /** 用户确认写操作后执行 */
  confirm: (data: { tool_name: string; tool_args: Record<string, any>; conversation_id: number }) =>
    api.post<any, AssistantConfirmResponse>('/assistant/confirm', data, { timeout: 60000 }),

  /** 对话列表 */
  getConversations: () => api.get<any, AssistantConversation[]>('/assistant/conversations'),

  /** 对话详情 */
  getConversation: (id: number) =>
    api.get<any, AssistantConversationDetail>(`/assistant/conversations/${id}`),

  /** 删除对话 */
  deleteConversation: (id: number) => api.delete(`/assistant/conversations/${id}`),

  /**
   * SSE 流式对话
   *
   * 使用原生 fetch + ReadableStream 实现 SSE，支持携带 Authorization header。
   */
  async chatStream(
    data: { message: string; conversation_id?: number },
    callbacks: {
      onChunk: (text: string) => void
      onToolCall?: (toolName: string) => void
      onPendingAction?: (action: PendingAction & { conversation_id: number }) => void
      onDone?: (conversationId?: number) => void
      onError?: (error: string) => void
    },
  ): Promise<void> {
    const token = localStorage.getItem('token') || ''
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''

    try {
      const response = await fetch(`${baseURL}/api/assistant/chat/stream`, {
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
      let conversationId: number | undefined

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const payload = line.slice(6)

          if (payload === '[DONE]') {
            callbacks.onDone?.(conversationId)
            return
          }

          if (payload.startsWith('[TOOL_CALL]')) {
            const toolName = payload.slice('[TOOL_CALL]'.length)
            callbacks.onToolCall?.(toolName)
            continue
          }

          if (payload.startsWith('[PENDING_ACTION]')) {
            try {
              const jsonStr = payload.slice('[PENDING_ACTION]'.length)
              const action = JSON.parse(jsonStr)
              conversationId = action.conversation_id
              callbacks.onPendingAction?.(action)
            } catch {
              // JSON 解析失败，忽略
            }
            continue
          }

          if (payload.startsWith('[ERROR]')) {
            callbacks.onError?.(payload.slice('[ERROR]'.length))
            return
          }

          // 普通文本块 — 还原后端转义的换行符
          callbacks.onChunk(payload.replace(/\\n/g, '\n'))
        }
      }

      callbacks.onDone?.(conversationId)
    } catch (err: any) {
      callbacks.onError?.(err?.message || '网络请求失败')
    }
  },
}
