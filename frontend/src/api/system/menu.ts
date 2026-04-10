// Menu API - 菜单管理模块
import api from '../index'
import type { Menu, MenuCreate, MenuUpdate } from './types'

export const menuApi = {
  getMyMenus: () => api.get<any, Menu[]>('/menus/my'),

  getMenus: () => api.get<any, Menu[]>('/menus/'),
  
  getAllMenus: (skip = 0, limit = 100) => api.get<any, Menu[]>('/menus/all', { params: { skip, limit } }),
  
  getMenu: (id: number) => api.get<any, Menu>(`/menus/${id}`),
  
  createMenu: (data: MenuCreate) => api.post<any, Menu>('/menus/', data),
  
  updateMenu: (id: number, data: MenuUpdate) => api.put<any, Menu>(`/menus/${id}`, data),
  
  deleteMenu: (id: number) => api.delete(`/menus/${id}`)
}
