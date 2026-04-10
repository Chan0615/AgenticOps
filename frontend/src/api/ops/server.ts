/**
 * 服务器管理 API
 */
import request from '@/api'

export interface Server {
  id: number
  name: string
  hostname: string
  port: number
  username: string
  salt_minion_id?: string
  environment: string
  tags?: string[]
  status: string
  description?: string
  created_by?: string
  created_at: string
  updated_at: string
}

export interface ServerListParams {
  page?: number
  page_size?: number
  name?: string
  environment?: string
  status?: string
}

export interface ServerListResponse {
  code: number
  message: string
  data: Server[]
  total: number
}

/**
 * 获取服务器列表
 */
export const getServerList = (params: ServerListParams) => {
  return request.get<any, ServerListResponse>('/ops/servers', { params })
}

/**
 * 获取服务器详情
 */
export const getServerDetail = (id: number) => {
  return request.get<any, Server>(`/ops/servers/${id}`)
}

/**
 * 创建服务器
 */
export const createServer = (data: Partial<Server>) => {
  return request.post<any, Server>('/ops/servers', data)
}

/**
 * 更新服务器
 */
export const updateServer = (id: number, data: Partial<Server>) => {
  return request.put<any, Server>(`/ops/servers/${id}`, data)
}

/**
 * 删除服务器
 */
export const deleteServer = (id: number) => {
  return request.delete<any>(`/ops/servers/${id}`)
}

/**
 * 测试服务器连接
 */
export const testServerConnection = (data: { server_id: number; test_type: string }) => {
  return request.post<any, { code: number; message: string; data?: any }>('/ops/servers/test-connection', data)
}
