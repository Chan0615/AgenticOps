// Agent RAG API
import api from '../index'

export const agentApi = {
  // 知识库
  getKnowledgeBases: () => api.get<any, any[]>('/agent/knowledge-bases'),
  createKnowledgeBase: (data: { name: string; description?: string }) => api.post<any, any>('/agent/knowledge-bases', data),
  getKnowledgeBase: (id: number) => api.get<any, any>(`/agent/knowledge-bases/${id}`),
  deleteKnowledgeBase: (id: number) => api.delete(`/agent/knowledge-bases/${id}`),

  // 文档
  getDocuments: (kbId: number) => api.get<any, any[]>(`/agent/knowledge-bases/${kbId}/documents`),
  createDocument: (kbId: number, data: { title: string; content: string; source?: string }) =>
    api.post<any, any>(`/agent/knowledge-bases/${kbId}/documents`, data),
  deleteDocument: (docId: number) => api.delete(`/agent/documents/${docId}`),

  // 对话
  chat: (data: { message: string; kb_id?: number; conversation_id?: number }) =>
    api.post<any, { answer?: string; sources?: string[]; conversation_id?: number }>('/agent/chat', data),
  getConversations: () => api.get<any, any[]>('/agent/conversations'),
  getConversation: (id: number) => api.get<any, any>(`/agent/conversations/${id}`),
  deleteConversation: (id: number) => api.delete(`/agent/conversations/${id}`),
}
