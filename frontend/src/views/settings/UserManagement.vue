<template>
  <div>
    <!-- 页头 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-surface-900">用户管理</h2>
        <p class="text-sm text-surface-400 mt-0.5">管理系统用户账号与权限</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="px-4 py-2.5 bg-gradient-to-r from-brand-500 to-brand-600 text-white text-sm font-medium rounded-xl shadow-lg shadow-brand-200/50 hover:shadow-brand-300/50 hover:from-brand-400 hover:to-brand-500 transition-all duration-200 flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        添加用户
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="bg-white rounded-2xl border border-surface-100 p-4 mb-6">
      <div class="flex flex-col md:flex-row gap-3">
        <div class="relative w-full md:w-72">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="搜索用户名或邮箱..."
            class="w-full h-10 pl-10 pr-4 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
          />
        </div>
        <select 
          v-model="statusFilter"
          class="h-10 px-4 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-700 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all appearance-none cursor-pointer"
        >
          <option value="">所有状态</option>
          <option value="true">正常</option>
          <option value="false">禁用</option>
        </select>
      </div>
    </div>

    <!-- 用户表格 -->
    <div class="bg-white rounded-2xl border border-surface-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-surface-100">
              <th class="px-6 py-4 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">用户</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">邮箱</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">角色</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">创建时间</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-surface-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-surface-50">
            <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-brand-50/30 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0">
                    <span class="text-white text-sm font-semibold">{{ user.username.charAt(0).toUpperCase() }}</span>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-surface-900">{{ user.username }}</div>
                    <div class="text-xs text-surface-400">{{ user.full_name || '-' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-surface-600">{{ user.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'px-2.5 py-1 text-xs font-medium rounded-lg',
                  user.is_superuser ? 'bg-brand-50 text-brand-700' : 'bg-surface-100 text-surface-600'
                ]">
                  {{ user.is_superuser ? '超级管理员' : '普通用户' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="flex items-center gap-1.5">
                  <span :class="['w-1.5 h-1.5 rounded-full', user.status ? 'bg-emerald-500' : 'bg-surface-300']"></span>
                  <span class="text-sm" :class="user.status ? 'text-surface-700' : 'text-surface-400'">{{ user.status ? '正常' : '禁用' }}</span>
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-surface-400">
                {{ formatDate(user.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <button 
                  @click="editUser(user)"
                  class="text-sm text-brand-500 hover:text-brand-700 font-medium mr-3 transition-colors"
                >编辑</button>
                <button 
                  v-if="currentUser?.is_superuser"
                  @click="showResetPassword(user)"
                  class="text-sm text-amber-500 hover:text-amber-700 font-medium mr-3 transition-colors"
                >重置密码</button>
                <button 
                  v-if="!user.is_superuser"
                  @click="deleteUser(user.id)"
                  class="text-sm text-surface-400 hover:text-rose-500 font-medium transition-colors"
                >删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 空状态 -->
      <div v-if="filteredUsers.length === 0" class="p-16 text-center">
        <div class="w-14 h-14 rounded-2xl bg-surface-50 border border-surface-100 flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <h3 class="text-sm font-medium text-surface-700">暂无用户</h3>
        <p class="text-xs text-surface-400 mt-1">点击上方「添加用户」开始创建</p>
      </div>
    </div>

    <!-- 添加/编辑模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md animate-fade-in">
        <!-- 模态框头部 -->
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-100">
          <h3 class="text-base font-semibold text-surface-900">{{ showEditModal ? '编辑用户' : '添加用户' }}</h3>
          <button @click="closeModal" class="w-8 h-8 rounded-lg hover:bg-surface-100 flex items-center justify-center transition-colors">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">用户名</label>
            <input 
              v-model="formData.username"
              type="text"
              required
              :disabled="showEditModal"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white disabled:bg-surface-100 disabled:text-surface-400 transition-all"
              placeholder="请输入用户名"
            />
          </div>
          
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">邮箱</label>
            <input 
              v-model="formData.email"
              type="email"
              required
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="请输入邮箱"
            />
          </div>
          
          <div v-if="!showEditModal">
            <label class="block text-xs font-medium text-surface-600 mb-1.5">密码</label>
            <input 
              v-model="formData.password"
              type="password"
              required
              minlength="6"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="至少6个字符"
            />
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-surface-600 mb-1.5">真实姓名</label>
              <input 
                v-model="formData.full_name"
                type="text"
                class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
                placeholder="选填"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-surface-600 mb-1.5">手机号</label>
              <input 
                v-model="formData.phone"
                type="text"
                class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
                placeholder="选填"
              />
            </div>
          </div>
          
          <div v-if="showEditModal">
            <label class="block text-xs font-medium text-surface-600 mb-1.5">状态</label>
            <select 
              v-model="formData.status"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-700 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
            >
              <option :value="true">正常</option>
              <option :value="false">禁用</option>
            </select>
          </div>
          
          <div class="flex justify-end gap-3 pt-4 border-t border-surface-100">
            <button 
              type="button"
              @click="closeModal"
              class="px-5 py-2.5 text-sm font-medium text-surface-600 bg-surface-50 border border-surface-200 rounded-xl hover:bg-surface-100 transition-colors"
            >取消</button>
            <button 
              type="submit"
              :disabled="loading"
              class="px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-brand-500 to-brand-600 rounded-xl shadow-lg shadow-brand-200/50 hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-50"
            >{{ loading ? '保存中...' : '保存' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 重置密码模态框 -->
    <div v-if="showResetPasswordModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeResetModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm animate-fade-in">
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-100">
          <h3 class="text-base font-semibold text-surface-900">重置密码</h3>
          <button @click="closeResetModal" class="w-8 h-8 rounded-lg hover:bg-surface-100 flex items-center justify-center transition-colors">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 space-y-4">
          <div class="flex items-center gap-3 p-3 bg-amber-50 border border-amber-100 rounded-xl">
            <svg class="w-5 h-5 text-amber-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <p class="text-sm font-medium text-amber-800">正在为 {{ resetPasswordUser?.username }} 重置密码</p>
              <p class="text-xs text-amber-600 mt-0.5">重置后请妥善保管新密码</p>
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">新密码</label>
            <input 
              v-model="newPassword"
              type="password"
              required
              minlength="6"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="至少6个字符"
            />
          </div>
          
          <div class="flex justify-end gap-3 pt-4 border-t border-surface-100">
            <button 
              type="button"
              @click="closeResetModal"
              class="px-5 py-2.5 text-sm font-medium text-surface-600 bg-surface-50 border border-surface-200 rounded-xl hover:bg-surface-100 transition-colors"
            >取消</button>
            <button 
              type="button"
              @click="handleResetPassword"
              :disabled="loading || !newPassword"
              class="px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl shadow-lg shadow-amber-200/50 hover:from-amber-400 hover:to-orange-400 transition-all disabled:opacity-50"
            >{{ loading ? '重置中...' : '确认重置' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { userApi } from '@/api/system/user'
import type { User, UserUpdate } from '@/api/system/types'
import { formatDateTime } from '@/utils/datetime'

const authStore = useAuthStore()
const currentUser = computed(() => authStore.user)

const users = ref<User[]>([])
const searchQuery = ref('')
const statusFilter = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const showResetPasswordModal = ref(false)
const loading = ref(false)
const editingUserId = ref<number | null>(null)
const resetPasswordUser = ref<User | null>(null)
const newPassword = ref('')

const formData = reactive({
  username: '',
  email: '',
  password: '',
  full_name: '',
  phone: '',
  status: true
})

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = searchQuery.value === '' || 
      user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = statusFilter.value === '' || 
      user.status.toString() === statusFilter.value
    return matchesSearch && matchesStatus
  })
})

const formatDate = (dateString: string) => formatDateTime(dateString)

function editUser(user: User) {
  editingUserId.value = user.id
  formData.username = user.username
  formData.email = user.email
  formData.full_name = user.full_name || ''
  formData.phone = user.phone || ''
  formData.status = user.status
  showEditModal.value = true
}

function closeModal() {
  showAddModal.value = false
  showEditModal.value = false
  editingUserId.value = null
  resetForm()
}

function resetForm() {
  formData.username = ''
  formData.email = ''
  formData.password = ''
  formData.full_name = ''
  formData.phone = ''
  formData.status = true
}

async function handleSubmit() {
  loading.value = true
  try {
    if (showEditModal.value && editingUserId.value) {
      const updateData: UserUpdate = {
        email: formData.email,
        full_name: formData.full_name || undefined,
        phone: formData.phone || undefined,
        status: formData.status
      }
      await userApi.updateUser(editingUserId.value, updateData)
    } else {
      await userApi.createUser({
        username: formData.username,
        email: formData.email,
        password: formData.password
      })
    }
    await fetchUsers()
    closeModal()
  } catch (error) {
    console.error('Failed to save user:', error)
  } finally {
    loading.value = false
  }
}

async function deleteUser(userId: number) {
  if (!confirm('确定要删除这个用户吗？')) return
  try {
    await userApi.deleteUser(userId)
    await fetchUsers()
  } catch (error) {
    console.error('Failed to delete user:', error)
  }
}

async function fetchUsers() {
  try {
    users.value = await userApi.getUsers()
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

function showResetPassword(user: User) {
  resetPasswordUser.value = user
  newPassword.value = ''
  showResetPasswordModal.value = true
}

function closeResetModal() {
  showResetPasswordModal.value = false
  resetPasswordUser.value = null
  newPassword.value = ''
}

async function handleResetPassword() {
  if (!resetPasswordUser.value || !newPassword.value) return
  
  loading.value = true
  try {
    await userApi.resetPassword(resetPasswordUser.value.id, newPassword.value)
    alert(`密码已重置成功！\n用户：${resetPasswordUser.value.username}\n新密码：${newPassword.value}`)
    closeResetModal()
  } catch (error) {
    console.error('Failed to reset password:', error)
    alert('密码重置失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
