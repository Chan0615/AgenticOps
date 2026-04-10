// User API - 用户管理模块
import api from '../index'
import type { User, UserUpdate } from './types'

export const userApi = {
  getUsers: (skip = 0, limit = 100) => api.get<any, User[]>('/users/', { params: { skip, limit } }),
  
  getUser: (id: number) => api.get<any, User>(`/users/${id}`),
  
  createUser: (data: { username: string; email: string; password: string }) => 
    api.post<any, User>('/users/', data),
  
  updateUser: (id: number, data: UserUpdate) => api.put<any, User>(`/users/${id}`, data),
  
  deleteUser: (id: number) => api.delete(`/users/${id}`),
  
  resetPassword: (id: number, password: string) => 
    api.post(`/users/${id}/reset-password`, { password })
}
