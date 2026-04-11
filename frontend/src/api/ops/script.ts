/**
 * 脚本管理 API
 */
import request from '@/api'

export interface Script {
  id: number
  name: string
  project_id?: number
  group_id?: number
  project_name?: string
  group_name?: string
  description?: string
  content?: string
  file_path?: string
  source_file_name?: string
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
  project_id?: number
  group_id?: number
}

export interface ScriptListResponse {
  code: number
  message: string
  data: Script[]
  total: number
}

export interface ScriptVersion {
  id: number
  script_id: number
  version_no: number
  file_path: string
  source_file_name?: string
  note?: string
  created_by?: string
  created_at: string
}

export interface ScriptVersionDetail extends ScriptVersion {
  content: string
}

export interface ScriptVersionListResponse {
  code: number
  message: string
  data: ScriptVersion[]
}

export interface ScriptVersionDiffResponse {
  code: number
  message: string
  from_version_id: number
  to_version_id: number
  diff: string
}

/**
 * 获取脚本列表
 */
export const getScriptList = (params: ScriptListParams) => {
  const safeParams = {
    ...params,
    page_size: Math.min(Math.max(params.page_size ?? 20, 1), 100),
  }
  return request.get<any, ScriptListResponse>('/ops/scripts', { params: safeParams })
}

export const getScriptVersions = (scriptId: number) => {
  return request.get<any, ScriptVersionListResponse>(`/ops/scripts/${scriptId}/versions`)
}

export const getScriptVersionDetail = (scriptId: number, versionId: number) => {
  return request.get<any, ScriptVersionDetail>(`/ops/scripts/${scriptId}/versions/${versionId}`)
}

export const compareScriptVersions = (scriptId: number, fromVersionId: number, toVersionId: number) => {
  return request.get<any, ScriptVersionDiffResponse>(`/ops/scripts/${scriptId}/versions/compare`, {
    params: {
      from_version_id: fromVersionId,
      to_version_id: toVersionId,
    },
  })
}

export const rollbackScriptVersion = (scriptId: number, data: { version_id: number; note?: string }) => {
  return request.post<any, Script>(`/ops/scripts/${scriptId}/rollback`, data)
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
