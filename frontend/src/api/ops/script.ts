/**
 * 脚本管理 API
 */
import request from '@/api'

export interface Script {
  id: number
  name: string
  description?: string
  content?: string
  file_path?: string
  script_type: string
  parameters?: any[]
  timeout: number
  created_by?: string
  created_at: string
  updated_at: string
}

export interface ScriptDistributeRequest {
  server_ids: number[]
  target_directory: string
  file_name?: string
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
 * 上传脚本文件
 */
export const uploadScript = (formData: FormData) => {
  return request.post<any, Script>('/ops/scripts/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

/**
 * 重新上传脚本文件（更新已有脚本）
 */
export const replaceScriptFile = (id: number, formData: FormData) => {
  return request.post<any, Script>(`/ops/scripts/${id}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
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

/**
 * 分发脚本到目标服务器目录
 */
export const distributeScript = (scriptId: number, data: ScriptDistributeRequest) => {
  return request.post<any, { code: number; message: string; data?: any }>(`/ops/scripts/${scriptId}/distribute`, data)
}
