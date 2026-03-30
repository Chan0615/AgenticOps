// Menu API - 菜单管理模块
import api from '../index'
import type { Menu, MenuCreate, MenuUpdate } from './types'

export const menuApi = {
  getMyMenus: () => api.get<Menu[]>('/menus/my'),

  getMenus: () => api.get<Menu[]>('/menus/'),
  
  getAllMenus: (skip = 0, limit = 100) => api.get<Menu[]>('/menus/all', { params: { skip, limit } }),
  
  getMenu: (id: number) => api.get<Menu>(`/menus/${id}`),
  
  createMenu: (data: MenuCreate) => api.post<Menu>('/menus/', data),
  
  updateMenu: (id: number, data: MenuUpdate) => api.put<Menu>(`/menus/${id}`, data),
  
  deleteMenu: (id: number) => api.delete(`/menus/${id}`)
}
