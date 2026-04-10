import api from './index'

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
  created_at?: string
}

export interface AssistantConversationDetail extends AssistantConversation {
  messages: AssistantMessage[]
}

export const assistantApi = {
  chat: (data: { message: string; conversation_id?: number }) =>
    api.post<any, { answer?: string; conversation_id?: number }>('/rag/chat', data),
  getConversations: () => api.get<any, AssistantConversation[]>('/rag/conversations'),
  getConversation: (id: number) => api.get<any, AssistantConversationDetail>(`/rag/conversations/${id}`),
  deleteConversation: (id: number) => api.delete(`/rag/conversations/${id}`),
}
