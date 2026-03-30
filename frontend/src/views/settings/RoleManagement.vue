<template>
  <div>
    <!-- 页头 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-surface-900">角色管理</h2>
        <p class="text-sm text-surface-400 mt-0.5">配置角色与菜单权限</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="px-4 py-2.5 bg-gradient-to-r from-brand-500 to-brand-600 text-white text-sm font-medium rounded-xl shadow-lg shadow-brand-200/50 hover:shadow-brand-300/50 hover:from-brand-400 hover:to-brand-500 transition-all duration-200 flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        添加角色
      </button>
    </div>

    <!-- 角色卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="role in roles" 
        :key="role.id"
        class="bg-white rounded-2xl border border-surface-100 p-5 hover:border-brand-200 hover:shadow-lg hover:shadow-brand-100/50 transition-all duration-300"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-brand-50 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-semibold text-surface-900">{{ role.name }}</h3>
              <p class="text-xs text-surface-400">{{ role.code }}</p>
            </div>
          </div>
          <span class="flex items-center gap-1.5">
            <span :class="['w-1.5 h-1.5 rounded-full', role.status ? 'bg-emerald-500' : 'bg-surface-300']"></span>
            <span class="text-xs" :class="role.status ? 'text-surface-600' : 'text-surface-400'">{{ role.status ? '正常' : '禁用' }}</span>
          </span>
        </div>
        
        <p class="text-sm text-surface-500 mb-3 min-h-[20px]">{{ role.description || '暂无描述' }}</p>
        
        <div class="flex items-center gap-1.5 mb-4">
          <span class="text-xs text-surface-400">已授权 {{ (role.menu_ids || []).length }} 项</span>
          <span class="text-surface-300">·</span>
          <span class="text-xs text-surface-400">排序 {{ role.sort_order }}</span>
        </div>
        
        <div class="flex gap-2 pt-4 border-t border-surface-100">
          <button 
            @click="openPermDrawer(role)"
            class="flex-1 px-3 py-2 text-xs font-medium text-brand-600 bg-brand-50 hover:bg-brand-100 rounded-xl transition-colors flex items-center justify-center gap-1.5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            配置权限
          </button>
          <button 
            @click="openUsersDrawer(role)"
            class="px-3 py-2 text-xs font-medium text-surface-600 bg-surface-50 hover:bg-surface-100 rounded-xl transition-colors flex items-center gap-1"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            用户
          </button>
          <button 
            @click="editRole(role)"
            class="px-3 py-2 text-xs font-medium text-surface-600 bg-surface-50 hover:bg-surface-100 rounded-xl transition-colors"
          >编辑</button>
          <button 
            @click="deleteRole(role.id)"
            class="px-3 py-2 text-xs font-medium text-surface-400 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition-colors"
          >删除</button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="roles.length === 0" class="bg-white rounded-2xl border border-surface-100 p-16 text-center">
      <div class="w-14 h-14 rounded-2xl bg-surface-50 border border-surface-100 flex items-center justify-center mx-auto mb-4">
        <svg class="w-7 h-7 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      </div>
      <h3 class="text-sm font-medium text-surface-700">暂无角色</h3>
      <p class="text-xs text-surface-400 mt-1">点击上方「添加角色」开始创建</p>
    </div>

    <!-- 权限配置弹窗 -->
    <div v-if="showPermModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="showPermModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md animate-fade-in max-h-[80vh] flex flex-col">
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-100 shrink-0">
          <div>
            <h3 class="text-base font-semibold text-surface-900">配置权限</h3>
            <p class="text-xs text-surface-400 mt-0.5">{{ permRole?.name }}</p>
          </div>
          <button @click="showPermModal = false" class="w-8 h-8 rounded-lg hover:bg-surface-100 flex items-center justify-center">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <div v-if="menuTree.length === 0" class="text-center py-12 text-sm text-surface-400">暂无菜单</div>
          <div v-else class="space-y-1">
            <template v-for="menu in menuTree" :key="menu.id">
              <label class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-surface-50 cursor-pointer group">
                <input 
                  type="checkbox" 
                  :checked="checkedMenuIds.has(menu.id)"
                  :indeterminate="isIndeterminate(menu)"
                  @change="toggleMenu(menu)"
                  class="w-4 h-4 rounded border-surface-300 text-brand-500 focus:ring-brand-400 focus:ring-offset-0 accent-brand-500"
                />
                <span class="text-sm font-medium text-surface-800">{{ menu.name }}</span>
                <span class="text-[10px] px-1.5 py-0.5 bg-surface-100 text-surface-400 rounded ml-auto">{{ menu.code }}</span>
              </label>
              <div v-if="menu.children?.length" class="ml-6 space-y-0.5">
                <label 
                  v-for="child in menu.children" 
                  :key="child.id"
                  class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-surface-50 cursor-pointer"
                >
                  <input 
                    type="checkbox" 
                    :checked="checkedMenuIds.has(child.id)"
                    @change="toggleMenu(child)"
                    class="w-4 h-4 rounded border-surface-300 text-brand-500 focus:ring-brand-400 focus:ring-offset-0 accent-brand-500"
                  />
                  <span class="text-sm text-surface-600">{{ child.name }}</span>
                </label>
                <div v-for="child in menu.children" :key="'btn-'+child.id">
                  <div v-if="child.children?.length" class="ml-6 space-y-0.5 mt-0.5">
                    <label 
                      v-for="btn in child.children" 
                      :key="btn.id"
                      class="flex items-center gap-3 px-3 py-1.5 rounded-lg hover:bg-surface-50 cursor-pointer"
                    >
                      <input 
                        type="checkbox" 
                        :checked="checkedMenuIds.has(btn.id)"
                        @change="toggleMenu(btn)"
                        class="w-3.5 h-3.5 rounded border-surface-300 text-brand-500 focus:ring-brand-400 focus:ring-offset-0 accent-brand-500"
                      />
                      <span class="text-xs text-surface-500">{{ btn.name }}</span>
                    </label>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-surface-100 shrink-0 flex justify-between items-center">
          <span class="text-xs text-surface-400">已选 {{ checkedMenuIds.size }} 项</span>
          <div class="flex gap-3">
            <button 
              @click="showPermModal = false"
              class="px-5 py-2.5 text-sm font-medium text-surface-600 bg-surface-50 border border-surface-200 rounded-xl hover:bg-surface-100 transition-colors"
            >取消</button>
            <button 
              @click="savePermissions"
              :disabled="permSaving"
              class="px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-brand-500 to-brand-600 rounded-xl shadow-lg shadow-brand-200/50 hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-50"
            >{{ permSaving ? '保存中...' : '保存' }}</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 查看用户弹窗 -->
    <div v-if="showUsersModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="showUsersModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm animate-fade-in">
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-100">
          <div>
            <h3 class="text-base font-semibold text-surface-900">角色用户</h3>
            <p class="text-xs text-surface-400 mt-0.5">{{ usersRole?.name }} · {{ roleUsers.length }} 人</p>
          </div>
          <button @click="showUsersModal = false" class="w-8 h-8 rounded-lg hover:bg-surface-100 flex items-center justify-center">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-4 max-h-[60vh] overflow-y-auto">
          <div v-if="usersLoading" class="flex justify-center py-12">
            <svg class="animate-spin w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          </div>
          <div v-else-if="roleUsers.length === 0" class="text-center py-12">
            <svg class="w-10 h-10 text-surface-200 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p class="text-sm text-surface-400">暂无用户关联此角色</p>
          </div>
          <div v-else class="space-y-1">
            <div 
              v-for="user in roleUsers" 
              :key="user.id"
              class="flex items-center gap-3 px-3 py-3 rounded-xl hover:bg-surface-50 transition-colors"
            >
              <div class="w-9 h-9 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0">
                <span class="text-white text-sm font-semibold">{{ user.username.charAt(0).toUpperCase() }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-sm font-medium text-surface-900">{{ user.username }}</div>
                <div class="text-xs text-surface-400 truncate">{{ user.email }}</div>
              </div>
              <span :class="['w-2 h-2 rounded-full shrink-0', user.status ? 'bg-emerald-400' : 'bg-surface-300']"></span>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-surface-100">
          <button 
            @click="showUsersModal = false"
            class="w-full px-4 py-2.5 text-sm font-medium text-surface-600 bg-surface-50 border border-surface-200 rounded-xl hover:bg-surface-100 transition-colors"
          >关闭</button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑角色模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md animate-fade-in">
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-100">
          <h3 class="text-base font-semibold text-surface-900">{{ showEditModal ? '编辑角色' : '添加角色' }}</h3>
          <button @click="closeModal" class="w-8 h-8 rounded-lg hover:bg-surface-100 flex items-center justify-center">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">角色名称</label>
            <input v-model="formData.name" type="text" required
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="请输入角色名称" />
          </div>
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">角色代码</label>
            <input v-model="formData.code" type="text" required :disabled="showEditModal"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white disabled:bg-surface-100 disabled:text-surface-400 transition-all"
              placeholder="如: editor" />
          </div>
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">描述</label>
            <textarea v-model="formData.description" rows="2"
              class="w-full px-3.5 py-2.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all resize-none"
              placeholder="选填"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-surface-600 mb-1.5">排序</label>
              <input v-model.number="formData.sort_order" type="number"
                class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all" />
            </div>
            <div v-if="showEditModal">
              <label class="block text-xs font-medium text-surface-600 mb-1.5">状态</label>
              <select v-model="formData.status"
                class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-700 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all">
                <option :value="true">正常</option>
                <option :value="false">禁用</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4 border-t border-surface-100">
            <button type="button" @click="closeModal"
              class="px-5 py-2.5 text-sm font-medium text-surface-600 bg-surface-50 border border-surface-200 rounded-xl hover:bg-surface-100 transition-colors">取消</button>
            <button type="submit" :disabled="loading"
              class="px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-brand-500 to-brand-600 rounded-xl shadow-lg shadow-brand-200/50 hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-50">{{ loading ? '保存中...' : '保存' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { roleApi } from '@/api/system/role'
import { menuApi } from '@/api/system/menu'
import type { Role, RoleCreate, RoleUpdate, Menu } from '@/api/system/types'

const roles = ref<Role[]>([])
const menuTree = ref<Menu[]>([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const loading = ref(false)
const editingRoleId = ref<number | null>(null)

// 权限抽屉
const showPermModal = ref(false)
const permRole = ref<Role | null>(null)
const checkedMenuIds = ref(new Set<number>())
const permSaving = ref(false)

// 用户抽屉
const showUsersModal = ref(false)
const usersRole = ref<Role | null>(null)
const roleUsers = ref<any[]>([])
const usersLoading = ref(false)

async function openUsersDrawer(role: Role) {
  usersRole.value = role
  roleUsers.value = []
  usersLoading.value = true
  showUsersModal.value = true
  try {
    roleUsers.value = await roleApi.getRoleUsers(role.id)
  } catch (e) {
    console.error(e)
  } finally {
    usersLoading.value = false
  }
}

const formData = reactive({
  name: '', code: '', description: '', sort_order: 0, status: true
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
  formData.name = ''
  formData.code = ''
  formData.description = ''
  formData.sort_order = 0
  formData.status = true
}

// 权限配置
async function openPermDrawer(role: Role) {
  permRole.value = role
  checkedMenuIds.value = new Set(role.menu_ids || [])
  showPermModal.value = true
}

function toggleMenu(menu: Menu) {
  if (checkedMenuIds.value.has(menu.id)) {
    checkedMenuIds.value.delete(menu.id)
    // 取消选中时也取消所有子级
    if (menu.children) {
      const removeChildren = (items: Menu[]) => {
        for (const child of items) {
          checkedMenuIds.value.delete(child.id)
          if (child.children) removeChildren(child.children)
        }
      }
      removeChildren(menu.children)
    }
  } else {
    checkedMenuIds.value.add(menu.id)
    // 选中时也选中所有子级
    if (menu.children) {
      const addChildren = (items: Menu[]) => {
        for (const child of items) {
          checkedMenuIds.value.add(child.id)
          if (child.children) addChildren(child.children)
        }
      }
      addChildren(menu.children)
    }
  }
  // 触发响应式更新
  checkedMenuIds.value = new Set(checkedMenuIds.value)
}

function isIndeterminate(menu: Menu): boolean {
  if (!menu.children?.length) return false
  const childIds = getAllChildIds(menu)
  const checked = childIds.filter(id => checkedMenuIds.value.has(id))
  return checked.length > 0 && checked.length < childIds.length
}

function getAllChildIds(menu: Menu): number[] {
  const ids: number[] = []
  if (menu.children) {
    for (const child of menu.children) {
      ids.push(child.id)
      ids.push(...getAllChildIds(child))
    }
  }
  return ids
}

async function savePermissions() {
  if (!permRole.value) return
  permSaving.value = true
  try {
    await roleApi.updateRoleMenus(permRole.value.id, Array.from(checkedMenuIds.value))
    showPermModal.value = false
    await fetchRoles()
  } catch (e) {
    console.error(e)
  } finally {
    permSaving.value = false
  }
}

async function handleSubmit() {
  loading.value = true
  try {
    if (showEditModal.value && editingRoleId.value) {
      await roleApi.updateRole(editingRoleId.value, {
        name: formData.name, description: formData.description || undefined,
        sort_order: formData.sort_order, status: formData.status
      })
    } else {
      await roleApi.createRole({
        name: formData.name, code: formData.code,
        description: formData.description || undefined, sort_order: formData.sort_order
      })
    }
    await fetchRoles()
    closeModal()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function deleteRole(roleId: number) {
  if (!confirm('确定要删除这个角色吗？')) return
  try {
    await roleApi.deleteRole(roleId)
    await fetchRoles()
  } catch (e) {
    console.error(e)
  }
}

async function fetchRoles() {
  try {
    roles.value = await roleApi.getRoles()
  } catch (e) {
    console.error(e)
  }
}

async function fetchMenuTree() {
  try {
    menuTree.value = await menuApi.getMenus()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchRoles()
  fetchMenuTree()
})
</script>
