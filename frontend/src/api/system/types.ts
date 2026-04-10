// User types - 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  phone?: string
  full_name?: string
  avatar?: string
  status: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  phone?: string
  full_name?: string
}

export interface UserUpdate {
  email?: string
  phone?: string
  full_name?: string
  avatar?: string
  status?: boolean
}

// Menu types - 菜单相关类型
export interface Menu {
  id: number
  name: string
  code: string
  path?: string
  component?: string
  icon?: string
  parent_id?: number
  sort_order: number
  type: string
  status: boolean
  meta?: Record<string, any>
  description?: string
  children?: Menu[]
  created_at: string
  updated_at: string
}

export interface MenuCreate {
  name: string
  code: string
  path?: string
  component?: string
  icon?: string
  parent_id?: number
  sort_order?: number
  type?: string
  status?: boolean
  meta?: Record<string, any>
  description?: string
}

export interface MenuUpdate {
  name?: string
  path?: string
  component?: string
  icon?: string
  parent_id?: number
  sort_order?: number
  type?: string
  status?: boolean
  meta?: Record<string, any>
  description?: string
}

// Role types - 角色相关类型
export interface Role {
  id: number
  name: string
  code: string
  description?: string
  status: boolean
  sort_order: number
  menu_ids?: number[]
  created_at: string
  updated_at: string
}

export interface RoleCreate {
  name: string
  code: string
  description?: string
  status?: boolean
  sort_order?: number
}

export interface RoleUpdate {
  name?: string
  description?: string
  status?: boolean
  sort_order?: number
}
