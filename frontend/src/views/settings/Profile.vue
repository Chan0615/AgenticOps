<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900">个人设置</h1>
      <p class="text-sm text-surface-500 mt-1">管理你的个人信息和账户安全</p>
    </div>

    <!-- 个人信息卡片 -->
    <div class="bg-white rounded-2xl border border-surface-200 shadow-sm overflow-hidden mb-6">
      <!-- 头部背景 -->
      <div class="h-24 bg-gradient-to-r from-brand-400 via-brand-500 to-brand-600 relative">
        <div class="absolute inset-0 opacity-20">
          <div class="absolute top-4 left-10 w-20 h-20 bg-white rounded-full blur-2xl"></div>
          <div class="absolute bottom-2 right-20 w-16 h-16 bg-white rounded-full blur-xl"></div>
        </div>
      </div>
      
      <!-- 头像和信息 -->
      <div class="px-6 pb-6">
        <div class="relative -mt-12 mb-4 flex items-end justify-between">
          <div class="flex items-end gap-4">
            <div class="relative">
              <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shadow-xl shadow-brand-200/50 ring-4 ring-white">
                <span class="text-4xl font-bold text-white">{{ userInitial }}</span>
              </div>
              <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-green-400 rounded-full ring-2 ring-white flex items-center justify-center">
                <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            <div class="pb-1">
              <h2 class="text-xl font-bold text-surface-900">{{ authStore.user?.full_name || authStore.user?.username }}</h2>
              <div class="flex items-center gap-2 mt-1">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium" :class="authStore.user?.is_superuser ? 'bg-brand-50 text-brand-600' : 'bg-surface-100 text-surface-600'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="authStore.user?.is_superuser ? 'bg-brand-400' : 'bg-surface-400'"></span>
                  {{ authStore.user?.is_superuser ? '超级管理员' : '普通用户' }}
                </span>
                <span class="text-xs text-surface-400">·</span>
                <span class="text-xs text-surface-500">{{ authStore.user?.email || '未设置邮箱' }}</span>
              </div>
            </div>
          </div>
        </div>

        <form @submit.prevent="handleUpdateProfile" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="group">
              <label class="block text-xs font-semibold text-surface-500 uppercase tracking-wider mb-2">用户名</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input 
                  v-model="form.username" 
                  type="text" 
                  disabled
                  class="w-full pl-10 pr-4 py-2.5 bg-surface-50 border border-surface-200 rounded-xl text-surface-500 text-sm cursor-not-allowed"
                />
              </div>
              <p class="text-[11px] text-surface-400 mt-1.5 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                用户名不可修改
              </p>
            </div>
            <div class="group">
              <label class="block text-xs font-semibold text-surface-500 uppercase tracking-wider mb-2">显示名称</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <input 
                  v-model="form.full_name" 
                  type="text" 
                  placeholder="请输入显示名称"
                  class="w-full pl-10 pr-4 py-2.5 bg-white border border-surface-200 rounded-xl text-surface-900 text-sm focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
                />
              </div>
            </div>
          </div>

          <div class="group">
            <label class="block text-xs font-semibold text-surface-500 uppercase tracking-wider mb-2">邮箱地址</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-4 w-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <input 
                v-model="form.email" 
                type="email" 
                placeholder="请输入邮箱地址"
                class="w-full pl-10 pr-4 py-2.5 bg-white border border-surface-200 rounded-xl text-surface-900 text-sm focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
              />
            </div>
          </div>

          <div class="pt-2 flex justify-end">
            <button 
              type="submit"
              :disabled="saving"
              class="inline-flex items-center gap-2 px-6 py-2.5 bg-brand-500 text-white text-sm font-medium rounded-xl hover:bg-brand-600 hover:shadow-lg hover:shadow-brand-200/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ saving ? '保存中...' : '保存修改' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 修改密码卡片 -->
    <div class="bg-white rounded-2xl border border-surface-200 shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-surface-100 bg-surface-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-surface-100 flex items-center justify-center">
            <svg class="w-5 h-5 text-surface-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div>
            <h3 class="text-base font-semibold text-surface-900">修改密码</h3>
            <p class="text-xs text-surface-500">定期更换密码可以提高账户安全性</p>
          </div>
        </div>
      </div>
      
      <div class="p-6">
        <form @submit.prevent="handleChangePassword" class="space-y-5">
          <div>
            <label class="block text-xs font-semibold text-surface-500 uppercase tracking-wider mb-2">当前密码</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-4 w-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </div>
              <input 
                v-model="passwordForm.current_password" 
                type="password" 
                placeholder="请输入当前密码"
                class="w-full pl-10 pr-4 py-2.5 bg-white border border-surface-200 rounded-xl text-surface-900 text-sm focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-xs font-semibold text-surface-500 uppercase tracking-wider mb-2">新密码</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <input 
                  v-model="passwordForm.new_password" 
                  type="password" 
                  placeholder="请输入新密码"
                  class="w-full pl-10 pr-4 py-2.5 bg-white border border-surface-200 rounded-xl text-surface-900 text-sm focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
                />
              </div>
            </div>
            <div>
              <label class="block text-xs font-semibold text-surface-500 uppercase tracking-wider mb-2">确认新密码</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <input 
                  v-model="passwordForm.confirm_password" 
                  type="password" 
                  placeholder="请再次输入新密码"
                  class="w-full pl-10 pr-4 py-2.5 bg-white border border-surface-200 rounded-xl text-surface-900 text-sm focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
                />
              </div>
            </div>
          </div>

          <div class="pt-2 flex justify-end">
            <button 
              type="submit"
              :disabled="changingPassword"
              class="inline-flex items-center gap-2 px-6 py-2.5 bg-surface-800 text-white text-sm font-medium rounded-xl hover:bg-surface-900 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <svg v-if="changingPassword" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
              {{ changingPassword ? '修改中...' : '修改密码' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const userInitial = computed(() => {
  return authStore.user?.username?.charAt(0).toUpperCase() || 'U'
})

const form = ref({
  username: '',
  full_name: '',
  email: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const saving = ref(false)
const changingPassword = ref(false)

onMounted(() => {
  if (authStore.user) {
    form.value = {
      username: authStore.user.username || '',
      full_name: authStore.user.full_name || '',
      email: authStore.user.email || ''
    }
  }
})

async function handleUpdateProfile() {
  saving.value = true
  try {
    await new Promise(r => setTimeout(r, 500))
    alert('个人信息已更新')
  } catch (e) {
    alert('更新失败')
  } finally {
    saving.value = false
  }
}

async function handleChangePassword() {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    alert('两次输入的新密码不一致')
    return
  }
  
  changingPassword.value = true
  try {
    await new Promise(r => setTimeout(r, 500))
    alert('密码已修改')
    passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
  } catch (e) {
    alert('修改失败')
  } finally {
    changingPassword.value = false
  }
}
</script>
