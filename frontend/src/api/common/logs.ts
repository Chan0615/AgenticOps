import api from '@/api'

const BASE_URL = '/logs'

export interface OperationLog {
  id: number
  user_id?: number
  username?: string
  module: string
  action: string
  description?: string
  method?: string
  path?: string
  status_code?: number
  request_params?: Record<string, any>
  response_data?: Record<string, any>
  error_message?: string
  ip_address?: string
  user_agent?: string
  execution_time?: number
  created_at: string
}

export interface OperationLogListResponse {
  total: number
  items: OperationLog[]
  data?: OperationLog[]
}

// 获取操作日志列表
export async function getOperationLogs(params?: {
  skip?: number
  limit?: number
  module?: string
  username?: string
  start_time?: string
  end_time?: string
}) {
  return api.get<any, OperationLogListResponse>(BASE_URL, { params })
}

// 获取操作日志详情
export async function getOperationLog(logId: number) {
  return api.get<any, OperationLog>(`${BASE_URL}/${logId}`)
}
