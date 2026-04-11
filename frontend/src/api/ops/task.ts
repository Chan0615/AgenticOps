/**
 * 定时任务 API
 */
import request from '@/api'

export interface ScheduledTask {
  id: number
  name: string
  project_id?: number
  group_id?: number
  project_name?: string
  group_name?: string
  description?: string
  script_id?: number
  server_ids: number[]
  cron_expression: string
  task_type: 'salt'
  command?: string
  enabled: boolean
  celery_task_id?: string
  last_run_at?: string
  next_run_at?: string
  created_by?: string
  updated_by?: string
  created_at: string
  updated_at: string
}

export interface TaskListParams {
  page?: number
  page_size?: number
  name?: string
  enabled?: boolean
  project_id?: number
  group_id?: number
}

export interface TaskListResponse {
  code: number
  message: string
  data: ScheduledTask[]
  total: number
}

export interface TaskSchedulerHealthData {
  ok: boolean
  workers: string[]
  required_queues: string[]
  queue_consumers: Record<string, number>
  missing_queues: string[]
  beat_healthy: boolean
  detail: string
}

export interface TaskSchedulerHealthResponse {
  code: number
  message: string
  data: TaskSchedulerHealthData
}

export interface CronValidationData {
  valid: boolean
  cron_expression: string
  description_zh?: string
  error?: string
}

export interface CronValidationResponse {
  code: number
  message: string
  data: CronValidationData
}

export interface CronNaturalConvertResponse {
  code: number
  message: string
  data: {
    text: string
    cron_expression: string
    description_zh: string
  }
}

export interface CronPreviewResponse {
  code: number
  message: string
  data: {
    cron_expression: string
    start_time: string
    next_runs: string[]
  }
}

/**
 * 获取任务列表
 */
export const getTaskList = (params: TaskListParams) => {
  const safeParams = {
    ...params,
    page_size: Math.min(Math.max(params.page_size ?? 20, 1), 100),
  }
  return request.get<any, TaskListResponse>('/ops/tasks', { params: safeParams })
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

/**
 * 获取 worker/beat 健康状态
 */
export const getTaskSchedulerHealth = () => {
  return request.get<any, TaskSchedulerHealthResponse>('/ops/tasks/health')
}

/**
 * 手动触发一次调度扫描
 */
export const syncTaskSchedule = () => {
  return request.post<any>('/ops/tasks/sync')
}

/**
 * 校验 Cron 表达式
 */
export const validateTaskCron = (cronExpression: string) => {
  return request.post<any, CronValidationResponse>('/ops/tasks/cron/validate', {
    cron_expression: cronExpression,
  })
}

/**
 * Cron 中文描述
 */
export const describeTaskCron = (cronExpression: string) => {
  return request.post<any, CronValidationResponse>('/ops/tasks/cron/describe', {
    cron_expression: cronExpression,
  })
}

/**
 * 自然语言转换 Cron
 */
export const convertNaturalToTaskCron = (text: string) => {
  return request.post<any, CronNaturalConvertResponse>('/ops/tasks/cron/natural', {
    text,
  })
}

/**
 * 预览未来执行时间
 */
export const previewTaskCronRuns = (cronExpression: string, count = 7) => {
  return request.post<any, CronPreviewResponse>('/ops/tasks/cron/preview', {
    cron_expression: cronExpression,
    count,
  })
}
