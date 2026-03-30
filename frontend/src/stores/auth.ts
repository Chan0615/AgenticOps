import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, type LoginRequest, type RegisterRequest } from '@/api/system/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  
  const isAuthenticated = computed(() => !!token.value)
  const isSuperuser = computed(() => user.value?.is_superuser ?? false)
  
  async function login(credentials: LoginRequest) {
    try {
      const response = await authApi.login(credentials)
      token.value = response.access_token
      refreshToken.value = response.refresh_token
      user.value = response.user || null
      
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)
      
      return response
    } catch (error) {
      throw error
    }
  }
  
  async function register(data: RegisterRequest) {
    try {
      const response = await authApi.register(data)
      token.value = response.access_token
      refreshToken.value = response.refresh_token
      user.value = response.user || null
      
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)
      
      return response
    } catch (error) {
      throw error
    }
  }
  
  async function fetchUser() {
    try {
      const response = await authApi.getMe()
      user.value = response
    } catch (error) {
      logout()
      throw error
    }
  }
  
  async function updateProfile(data: Partial<User>) {
    try {
      const response = await authApi.updateMe(data)
      user.value = response
      return response
    } catch (error) {
      throw error
    }
  }
  
  function logout() {
    user.value = null
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }
  
  // 初始化时获取用户信息
  if (token.value) {
    fetchUser().catch(() => {
      logout()
    })
  }
  
  return {
    user,
    token,
    refreshToken,
    isAuthenticated,
    isSuperuser,
    login,
    register,
    fetchUser,
    updateProfile,
    logout
  }
})
