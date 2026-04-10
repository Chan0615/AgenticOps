import request from '@/api'

export interface ExecutionLog {
  id: number
  task_id?: number
  server_id?: number
  status: string
  command: string
  output?: string
  error?: string
  exit_code?: number
  started_at?: string
  finished_at?: string
  duration?: number
  created_at: string
}

export interface ExecutionLogListResponse {
  code: number
  message: string
  data: ExecutionLog[]
  total: number
}

export const getExecutionLogs = (params: Record<string, any>) => {
  return request.get<any, ExecutionLogListResponse>('/ops/logs/execution', { params })
}

export const getExecutionLogDetail = (id: number) => {
  return request.get<any, ExecutionLog>(`/ops/logs/execution/${id}`)
}
