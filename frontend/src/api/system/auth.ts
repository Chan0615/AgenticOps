// Auth API - 通用认证模块
import api from '../index'
import type { User, LoginRequest, RegisterRequest } from './types'

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user?: User
}

export const authApi = {
  login: (data: LoginRequest) => api.post<TokenResponse>('/auth/login', data),
  
  register: (data: RegisterRequest) => api.post<TokenResponse>('/auth/register', data),
  
  refresh: (refresh_token: string) => api.post<TokenResponse>('/auth/refresh', { refresh_token }),
  
  getMe: () => api.get<User>('/auth/me'),
  
  updateMe: (data: Partial<User>) => api.put<User>('/auth/me', data),
  
  changePassword: (oldPassword: string, newPassword: string) => 
    api.post('/auth/change-password', { old_password: oldPassword, new_password: newPassword })
}
