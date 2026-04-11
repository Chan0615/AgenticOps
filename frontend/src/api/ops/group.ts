import request from '@/api'

export interface OpsProject {
  id: number
  name: string
  code: string
  description?: string
  created_by?: string
  created_at: string
  updated_at: string
}

export interface OpsGroup {
  id: number
  project_id: number
  project_name?: string
  name: string
  description?: string
  created_by?: string
  created_at: string
  updated_at: string
}

export interface ProjectListParams {
  page?: number
  page_size?: number
  name?: string
}

export interface GroupListParams {
  page?: number
  page_size?: number
  project_id?: number
  name?: string
}

export interface OpsProjectListResponse {
  code: number
  message: string
  data: OpsProject[]
  total: number
}

export interface OpsGroupListResponse {
  code: number
  message: string
  data: OpsGroup[]
  total: number
}

export const getProjectList = (params: ProjectListParams) => {
  return request.get<any, OpsProjectListResponse>('/ops/projects', { params })
}

export const getGroupList = (params: GroupListParams) => {
  return request.get<any, OpsGroupListResponse>('/ops/groups', { params })
}

export const createProject = (data: { name: string; code: string; description?: string }) => {
  return request.post<any, OpsProject>('/ops/projects', data)
}

export const updateProject = (id: number, data: { name?: string; code?: string; description?: string }) => {
  return request.put<any, OpsProject>(`/ops/projects/${id}`, data)
}

export const deleteProject = (id: number) => {
  return request.delete<any>(`/ops/projects/${id}`)
}

export const createGroup = (data: { project_id: number; name: string; description?: string }) => {
  return request.post<any, OpsGroup>('/ops/groups', data)
}

export const updateGroup = (id: number, data: { project_id?: number; name?: string; description?: string }) => {
  return request.put<any, OpsGroup>(`/ops/groups/${id}`, data)
}

export const deleteGroup = (id: number) => {
  return request.delete<any>(`/ops/groups/${id}`)
}
