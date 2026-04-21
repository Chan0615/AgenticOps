/**
 * 运维 AI 助手 API 客户端
 *
 * 对应后端路由：/api/ops/ai/*
 */

import api from '@/api/index'

// ============ 类型定义 ============

export interface OpsChatRequest {
  message: string
  conversation_id?: number
}

export interface PendingAction {
  tool_name: string
  tool_args: Record<string, any>
  description: string
}

export interface OpsChatResponse {
  conversation_id: number
  answer: string
  pending_action: PendingAction | null
  sources: string[]
}

export interface OpsConfirmRequest {
  tool_name: string
  tool_args: Record<string, any>
  conversation_id: number
}

export interface OpsConfirmResponse {
  conversation_id: number
  answer: string
  success: boolean
}

export interface OpsConversation {
  id: number
  title: string
  created_at: string
  updated_at: string
}

export interface OpsMessage {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  sources?: string[] | null
  created_at?: string | null
}

export interface OpsConversationDetail {
  id: number
  title: string
  created_at: string
  updated_at: string
  messages: OpsMessage[]
}

// ============ API 方法 ============

export const opsAiApi = {
  /**
   * 发起运维 AI 对话（非流式）
   */
  async chat(data: OpsChatRequest): Promise<OpsChatResponse> {
    const res = await api.post<OpsChatResponse>('/ops/ai/chat', data, {
      timeout: 120000,
    })
    return res.data
  },

  /**
   * 用户确认写操作后执行
   */
  async confirm(data: OpsConfirmRequest): Promise<OpsConfirmResponse> {
    const res = await api.post<OpsConfirmResponse>('/ops/ai/confirm', data, {
      timeout: 60000,
    })
    return res.data
  },

  /**
   * 获取对话列表
   */
  async getConversations(): Promise<OpsConversation[]> {
    const res = await api.get<OpsConversation[]>('/ops/ai/conversations')
    return res.data
  },

  /**
   * 获取对话详情（含消息历史）
   */
  async getConversation(id: number): Promise<OpsConversationDetail> {
    const res = await api.get<OpsConversationDetail>(`/ops/ai/conversations/${id}`)
    return res.data
  },

  /**
   * 删除对话
   */
  async deleteConversation(id: number): Promise<void> {
    await api.delete(`/ops/ai/conversations/${id}`)
  },

  /**
   * 创建 SSE 流式对话连接
   *
   * 使用原生 fetch + ReadableStream 实现 SSE，
   * 支持携带 Authorization header（EventSource API 不支持自定义 header）。
   *
   * @param data 请求参数
   * @param onChunk 收到文本块时的回调
   * @param onToolCall 收到工具调用通知时的回调（tool_name）
   * @param onPendingAction 收到写操作待确认事件时的回调
   * @param onDone 流结束时的回调（带最终 conversation_id）
   * @param onError 发生错误时的回调
   */
  async chatStream(
    data: OpsChatRequest,
    callbacks: {
      onChunk: (text: string) => void
      onToolCall?: (toolName: string) => void
      onPendingAction?: (action: PendingAction & { conversation_id: number }) => void
      onDone?: (conversationId?: number) => void
      onError?: (error: string) => void
    },
  ): Promise<void> {
    const token = localStorage.getItem('access_token') || ''
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''

    try {
      const response = await fetch(`${baseURL}/api/ops/ai/chat/stream`, {
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

          // 普通文本块
          callbacks.onChunk(payload)
        }
      }

      callbacks.onDone?.(conversationId)
    } catch (err: any) {
      callbacks.onError?.(err?.message || '网络请求失败')
    }
  },
}
