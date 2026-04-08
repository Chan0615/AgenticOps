/**
 * 脚本管理 API
 */
import request from '@/api'

export interface Script {
  id: number
  name: string
  description?: string
  content: string
  script_type: string
  parameters?: any[]
  timeout: number
  created_by?: string
  created_at: string
  updated_at: string
}

export interface ScriptListParams {
  page?: number
  page_size?: number
  name?: string
  script_type?: string
}

export interface ScriptListResponse {
  code: number
  message: string
  data: Script[]
  total: number
}

/**
 * 获取脚本列表
 */
export const getScriptList = (params: ScriptListParams) => {
  return request.get<any, ScriptListResponse>('/ops/scripts', { params })
}

/**
 * 获取脚本详情
 */
export const getScriptDetail = (id: number) => {
  return request.get<any, Script>(`/ops/scripts/${id}`)
}

/**
 * 创建脚本
 */
export const createScript = (data: Partial<Script>) => {
  return request.post<any, Script>('/ops/scripts', data)
}

/**
 * 更新脚本
 */
export const updateScript = (id: number, data: Partial<Script>) => {
  return request.put<any, Script>(`/ops/scripts/${id}`, data)
}

/**
 * 删除脚本
 */
export const deleteScript = (id: number) => {
  return request.delete<any>(`/ops/scripts/${id}`)
}

/**
 * 测试执行脚本
 */
export const testScript = (data: { script_id: number; server_id?: number; parameters?: any }) => {
  return request.post<any>('/ops/scripts/test', data)
}
