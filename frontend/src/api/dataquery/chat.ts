/**
 * 智能问数对话 API 客户端
 *
 * 支持 SSE 流式输出，自定义事件协议
 */

import api from '../index'

// ============ 类型定义 ============

export interface QueryAskRequest {
  datasource_id: number
  question: string
  conversation_history?: { role: string; content: string }[]
}

export interface QueryResult {
  columns: string[]
  rows: Record<string, any>[]
  row_count: number
  execution_time: number
  chart_type: string
  chart_config?: Record<string, any>
  has_more: boolean
}

export interface QueryHistory {
  id: number
  datasource_id: number
  question: string
  generated_sql?: string
  result_summary?: string
  row_count: number
  execution_time?: number
  status: string
  chart_type?: string
  error_message?: string
  created_at: string
}

export interface QueryHistoryDetail extends QueryHistory {
  result_data?: Record<string, any>[]
  chart_config?: Record<string, any>
}

export interface QueryHistoryListResponse {
  code: number
  message: string
  data: QueryHistory[]
  total: number
}

// ============ API 方法 ============

export const dataqueryApi = {
  /** 非流式查询 */
  ask: (data: QueryAskRequest) =>
    api.post<any, any>('/dataquery/chat/ask', data, { timeout: 120000 }),

  /** 查询历史列表 */
  getHistory: (params?: { page?: number; page_size?: number; datasource_id?: number }) =>
    api.get<any, QueryHistoryListResponse>('/dataquery/chat/history', { params }),

  /** 查询历史详情 */
  getHistoryDetail: (id: number) =>
    api.get<any, QueryHistoryDetail>(`/dataquery/chat/history/${id}`),

  /** 删除查询记录 */
  deleteHistory: (id: number) => api.delete(`/dataquery/chat/history/${id}`),

  /** 导出 Excel（返回下载链接） */
  getExportUrl: (historyId: number) => `/api/dataquery/chat/export/${historyId}`,

  /**
   * SSE 流式问数
   *
   * 事件协议：
   * - [SQL]{json}        — 生成的 SQL + 解释
   * - [EXECUTING]        — 正在执行
   * - [RESULT]{json}     — 查询结果
   * - 普通文本            — AI 摘要流式输出
   * - [DONE]{json}       — 完成（含 history_id）
   * - [ERROR]msg         — 错误
   */
  async askStream(
    data: QueryAskRequest,
    callbacks: {
      onSQL?: (info: { sql: string; explanation: string }) => void
      onExecuting?: () => void
      onResult?: (result: QueryResult) => void
      onSummaryChunk?: (text: string) => void
      onDone?: (info: { history_id: number }) => void
      onError?: (error: string) => void
    },
  ): Promise<void> {
    const token = localStorage.getItem('token') || ''
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''

    try {
      const response = await fetch(`${baseURL}/api/dataquery/chat/ask/stream`, {
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

          if (payload.startsWith('[SQL]')) {
            try {
              const info = JSON.parse(payload.slice('[SQL]'.length))
              callbacks.onSQL?.(info)
            } catch { /* ignore */ }
            continue
          }

          if (payload === '[EXECUTING]') {
            callbacks.onExecuting?.()
            continue
          }

          if (payload.startsWith('[RESULT]')) {
            try {
              const result = JSON.parse(payload.slice('[RESULT]'.length))
              callbacks.onResult?.(result)
            } catch { /* ignore */ }
            continue
          }

          if (payload.startsWith('[DONE]')) {
            try {
              const info = JSON.parse(payload.slice('[DONE]'.length))
              callbacks.onDone?.(info)
            } catch {
              callbacks.onDone?.({ history_id: 0 })
            }
            return
          }

          if (payload.startsWith('[ERROR]')) {
            callbacks.onError?.(payload.slice('[ERROR]'.length))
            return
          }

          // 普通文本 — AI 摘要流式输出
          callbacks.onSummaryChunk?.(payload.replace(/\\n/g, '\n'))
        }
      }

      callbacks.onDone?.({ history_id: 0 })
    } catch (err: any) {
      callbacks.onError?.(err?.message || '网络请求失败')
    }
  },
}
