<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800">角色管理</h2>
      <button 
        @click="showAddModal = true"
        class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        添加角色
      </button>
    </div>

    <!-- 角色列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="role in roles" 
        :key="role.id"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-800">{{ role.name }}</h3>
              <p class="text-sm text-gray-500">{{ role.code }}</p>
            </div>
          </div>
          <span 
            :class="[
              'px-2 py-1 text-xs font-medium rounded-full',
              role.status ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]"
          >
            {{ role.status ? '正常' : '禁用' }}
          </span>
        </div>
        
        <p class="text-sm text-gray-600 mb-4">{{ role.description || '暂无描述' }}</p>
        
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <span class="text-xs text-gray-400">
            排序: {{ role.sort_order }}
          </span>
          <div class="flex space-x-2">
            <button 
              @click="editRole(role)"
              class="px-3 py-1 text-sm text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
            >
              编辑
            </button>
            <button 
              @click="deleteRole(role.id)"
              class="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="roles.length === 0" class="bg-white rounded-xl shadow-sm p-12 text-center border border-gray-100">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">没有角色</h3>
      <p class="mt-1 text-sm text-gray-500">开始添加第一个角色吧。</p>
    </div>

    <!-- 添加/编辑角色模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800">{{ showEditModal ? '编辑角色' : '添加角色' }}</h3>
        </div>
        
        <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">角色名称</label>
            <input 
              v-model="formData.name"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">角色代码</label>
            <input 
              v-model="formData.code"
              type="text"
              required
              :disabled="showEditModal"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-100"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <textarea 
              v-model="formData.description"
              rows="3"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">排序</label>
            <input 
              v-model.number="formData.sort_order"
              type="number"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          
          <div v-if="showEditModal">
            <label class="block text-sm font-medium text-gray-700 mb-1">状态</label>
            <select 
              v-model="formData.status"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option :value="true">正常</option>
              <option :value="false">禁用</option>
            </select>
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button 
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              取消
            </button>
            <button 
              type="submit"
              :disabled="loading"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
            >
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { roleApi } from '@/api/system/role'
import type { Role, RoleCreate, RoleUpdate } from '@/api/system/types'

const roles = ref<Role[]>([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const loading = ref(false)
const editingRoleId = ref<number | null>(null)

const formData = reactive({
  name: '',
  code: '',
  description: '',
  sort_order: 0,
  status: true
})

function editRole(role: Role) {
  editingRoleId.value = role.id
  formData.name = role.name
  formData.code = role.code
  formData.description = role.description || ''
  formData.sort_order = role.sort_order
  formData.status = role.status
  showEditModal.value = true
}

function closeModal() {
  showAddModal.value = false
  showEditModal.value = false
  editingRoleId.value = null
  resetForm()
}

function resetForm() {
  formData.name = ''
  formData.code = ''
  formData.description = ''
  formData.sort_order = 0
  formData.status = true
}

async function handleSubmit() {
  loading.value = true
  try {
    if (showEditModal.value && editingRoleId.value) {
      const updateData: RoleUpdate = {
        name: formData.name,
        description: formData.description || undefined,
        sort_order: formData.sort_order,
        status: formData.status
      }
      await roleApi.updateRole(editingRoleId.value, updateData)
    } else {
      const createData: RoleCreate = {
        name: formData.name,
        code: formData.code,
        description: formData.description || undefined,
        sort_order: formData.sort_order
      }
      await roleApi.createRole(createData)
    }
    await fetchRoles()
    closeModal()
  } catch (error) {
    console.error('Failed to save role:', error)
    alert('保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

async function deleteRole(roleId: number) {
  if (!confirm('确定要删除这个角色吗？')) return
  
  try {
    await roleApi.deleteRole(roleId)
    await fetchRoles()
  } catch (error) {
    console.error('Failed to delete role:', error)
    alert('删除失败，请稍后重试')
  }
}

async function fetchRoles() {
  try {
    roles.value = await roleApi.getRoles()
  } catch (error) {
    console.error('Failed to fetch roles:', error)
  }
}

onMounted(() => {
  fetchRoles()
})
</script>
