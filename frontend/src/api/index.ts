import axios from 'axios'
// import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token，避免 Pinia 未初始化的问题
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // 只在登录页面以外的页面才跳转
      if (window.location.pathname !== '/login') {
        // 清除过期 token
        localStorage.removeItem('token')
        // 显示提示
        console.warn('登录已过期，请重新登录')
        // 跳转到登录页
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api
