import axios from 'axios'

const BASE_URL = '/api/server'

// ============ 服务器管理 ============

export interface Server {
  id: number
  name: string
  hostname: string
  port: number
  username: string
  os_type: string
  group_id?: number
  salt_minion_id?: string
  tags?: Record<string, any>
  status: boolean
  is_connected?: boolean
  last_connected_at?: string
  created_at: string
  updated_at: string
}

export interface ServerCreate {
  name: string
  hostname: string
  port?: number
  username: string
  password?: string
  private_key?: string
  os_type?: string
  group_id?: number
  environment?: string  // 环境标识（与 group_id 二选一）
  salt_minion_id?: string
  tags?: Record<string, any>
}

export interface ServerUpdate {
  name?: string
  hostname?: string
  port?: number
  username?: string
  password?: string
  private_key?: string
  os_type?: string
  group_id?: number
  salt_minion_id?: string
  tags?: Record<string, any>
  status?: boolean
}

export interface ServerListResponse {
  total: number
  items: Server[]
}

export interface ConnectivityCheckResponse {
  server_id: number
  hostname: string
  is_connected: boolean
  response_time?: number
  error_message?: string
}

// 获取服务器列表
export async function getServers(params?: {
  skip?: number
  limit?: number
  search?: string
  environment?: string
  status?: boolean
}) {
  return axios.get<ServerListResponse>(`${BASE_URL}/`, { params })
}

// 获取服务器详情
export async function getServer(serverId: number) {
  return axios.get<Server>(`${BASE_URL}/${serverId}`)
}

// 创建服务器
export async function createServer(data: ServerCreate) {
  return axios.post<Server>(`${BASE_URL}/`, data)
}

// 更新服务器
export async function updateServer(serverId: number, data: ServerUpdate) {
  return axios.put<Server>(`${BASE_URL}/${serverId}`, data)
}

// 删除服务器
export async function deleteServer(serverId: number) {
  return axios.delete(`${BASE_URL}/${serverId}`)
}

// 检测单个服务器连通性
export async function checkConnectivity(serverId: number) {
  return axios.post<ConnectivityCheckResponse>(`${BASE_URL}/${serverId}/check-connectivity`)
}

// ============ 服务器分组 ============

export interface ServerGroup {
  id: number
  name: string
  environment: string
  description?: string
  status: boolean
  created_at: string
  updated_at: string
}

export async function getServerGroups() {
  return axios.get<ServerGroup[]>(`${BASE_URL}/groups`)
}

export async function createServerGroup(data: { name: string; environment: string; description?: string }) {
  return axios.post<ServerGroup>(`${BASE_URL}/groups`, data)
}

// ============ SaltStack 管理 ============

export async function saltExecute(
  envName: string,
  target: string,
  fun: string,
  arg?: string[]
) {
  const params = new URLSearchParams()
  if (arg) arg.forEach(a => params.append('arg', a))
  
  return axios.post(`${BASE_URL}/salt/${envName}/execute`, null, {
    params: { target, fun, ...params }
  })
}

export async function saltGetMinions(envName: string) {
  return axios.get(`${BASE_URL}/salt/${envName}/minions`)
}

export async function saltPing(envName: string, target = '*') {
  return axios.post(`${BASE_URL}/salt/${envName}/ping`, null, {
    params: { target }
  })
}

export async function saltRunCommand(
  envName: string,
  target: string,
  command: string
) {
  return axios.post(`${BASE_URL}/salt/${envName}/command`, null, {
    params: { target, command }
  })
}

// ============ SSH 管理 ============

export interface SSHExecuteParams {
  server_id: string
  hostname: string
  command: string
  port?: number
  username?: string
  password?: string
  private_key?: string
}

export async function sshExecute(params: SSHExecuteParams) {
  return axios.post(`${BASE_URL}/ssh/execute`, null, { params })
}

export async function sshDisconnect(serverId: string) {
  return axios.post(`${BASE_URL}/ssh/disconnect/${serverId}`)
}

// ============ WebSocket SSH ============

export function getWebSocketUrl(): string {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${window.location.hostname}:8765`
}
