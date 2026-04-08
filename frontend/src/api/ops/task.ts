/**
 * 定时任务 API
 */
import request from '@/api'

export interface ScheduledTask {
  id: number
  name: string
  description?: string
  script_id?: number
  server_ids: number[]
  cron_expression: string
  task_type: string
  command?: string
  enabled: boolean
  celery_task_id?: string
  last_run_at?: string
  next_run_at?: string
  created_by?: string
  created_at: string
  updated_at: string
}

export interface TaskListParams {
  page?: number
  page_size?: number
  name?: string
  enabled?: boolean
}

export interface TaskListResponse {
  code: number
  message: string
  data: ScheduledTask[]
  total: number
}

/**
 * 获取任务列表
 */
export const getTaskList = (params: TaskListParams) => {
  return request.get<any, TaskListResponse>('/ops/tasks', { params })
}

/**
 * 获取任务详情
 */
export const getTaskDetail = (id: number) => {
  return request.get<any, ScheduledTask>(`/ops/tasks/${id}`)
}

/**
 * 创建任务
 */
export const createTask = (data: Partial<ScheduledTask>) => {
  return request.post<any, ScheduledTask>('/ops/tasks', data)
}

/**
 * 更新任务
 */
export const updateTask = (id: number, data: Partial<ScheduledTask>) => {
  return request.put<any, ScheduledTask>(`/ops/tasks/${id}`, data)
}

/**
 * 删除任务
 */
export const deleteTask = (id: number) => {
  return request.delete<any>(`/ops/tasks/${id}`)
}

/**
 * 切换任务启用状态
 */
export const toggleTask = (id: number) => {
  return request.post<any>(`/ops/tasks/${id}/toggle`)
}

/**
 * 手动触发任务执行
 */
export const triggerTask = (taskId: number) => {
  return request.post<any>('/ops/tasks/trigger', { task_id: taskId })
}
