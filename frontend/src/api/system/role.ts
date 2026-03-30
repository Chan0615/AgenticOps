// Role API - 角色管理模块
import api from '../index'
import type { Role, RoleCreate, RoleUpdate } from './types'

export const roleApi = {
  getRoles: (skip = 0, limit = 100) => api.get<Role[]>('/roles/', { params: { skip, limit } }),
  
  getRole: (id: number) => api.get<Role>(`/roles/${id}`),
  
  createRole: (data: RoleCreate) => api.post<Role>('/roles/', data),
  
  updateRole: (id: number, data: RoleUpdate) => api.put<Role>(`/roles/${id}`, data),
  
  deleteRole: (id: number) => api.delete(`/roles/${id}`)
}
