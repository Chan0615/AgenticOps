<template>
  <div>
    <!-- 页头 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-surface-900">菜单管理</h2>
        <p class="text-sm text-surface-400 mt-0.5">配置系统导航与权限菜单</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="px-4 py-2.5 bg-gradient-to-r from-brand-500 to-brand-600 text-white text-sm font-medium rounded-xl shadow-lg shadow-brand-200/50 hover:shadow-brand-300/50 hover:from-brand-400 hover:to-brand-500 transition-all duration-200 flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        添加菜单
      </button>
    </div>

    <!-- 菜单树 -->
    <div class="bg-white rounded-2xl border border-surface-100 overflow-hidden">
      <!-- 空状态 -->
      <div v-if="menuTree.length === 0" class="p-16 text-center">
        <div class="w-14 h-14 rounded-2xl bg-surface-50 border border-surface-100 flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
        </div>
        <h3 class="text-sm font-medium text-surface-700">暂无菜单</h3>
        <p class="text-xs text-surface-400 mt-1">点击上方「添加菜单」开始创建</p>
      </div>

      <!-- 菜单列表 -->
      <div v-else class="divide-y divide-surface-100">
        <template v-for="menu in menuTree" :key="menu.id">
          <!-- 一级菜单 -->
          <div class="flex items-center gap-4 px-6 py-4 hover:bg-brand-50/30 transition-colors group">
            <button 
              v-if="menu.children?.length"
              @click="toggleExpand(menu.id)"
              class="w-6 h-6 rounded-lg hover:bg-surface-100 flex items-center justify-center shrink-0 transition-colors"
            >
              <svg 
                :class="['w-3.5 h-3.5 text-surface-400 transition-transform duration-200', expandedMenus.has(menu.id) ? 'rotate-90' : '']"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
            <div v-else class="w-6"></div>

            <div class="w-9 h-9 rounded-xl bg-brand-50 flex items-center justify-center shrink-0">
              <span class="text-sm font-semibold text-brand-600">{{ menu.name.charAt(0) }}</span>
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-sm font-medium text-surface-900">{{ menu.name }}</span>
                <span class="px-1.5 py-0.5 text-[10px] bg-surface-100 text-surface-500 rounded">{{ menu.code }}</span>
                <span :class="[
                  'px-1.5 py-0.5 text-[10px] rounded',
                  menu.type === 'directory' ? 'bg-amber-50 text-amber-600' : menu.type === 'menu' ? 'bg-brand-50 text-brand-600' : 'bg-surface-50 text-surface-500'
                ]">{{ menu.type === 'directory' ? '目录' : menu.type === 'menu' ? '菜单' : '按钮' }}</span>
              </div>
              <p class="text-xs text-surface-400 mt-0.5 truncate">{{ menu.path || menu.description || '-' }}</p>
            </div>

            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button 
                v-if="menu.type !== 'button'"
                @click="addChildMenu(menu)"
                class="px-2.5 py-1.5 text-xs font-medium text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
              >添加子项</button>
              <button 
                @click="editMenu(menu)"
                class="px-2.5 py-1.5 text-xs font-medium text-surface-600 hover:bg-surface-100 rounded-lg transition-colors"
              >编辑</button>
              <button 
                @click="deleteMenu(menu.id)"
                class="px-2.5 py-1.5 text-xs font-medium text-surface-400 hover:text-rose-500 hover:bg-rose-50 rounded-lg transition-colors"
              >删除</button>
            </div>
          </div>

          <!-- 二级菜单 -->
          <div v-if="expandedMenus.has(menu.id) && menu.children?.length">
            <div 
              v-for="child in menu.children" 
              :key="child.id"
              class="flex items-center gap-4 pl-16 pr-6 py-3 hover:bg-brand-50/30 transition-colors group border-t border-surface-50"
            >
              <button 
                v-if="child.children?.length"
                @click="toggleExpand(child.id)"
                class="w-6 h-6 rounded-lg hover:bg-surface-100 flex items-center justify-center shrink-0"
              >
                <svg 
                  :class="['w-3.5 h-3.5 text-surface-400 transition-transform duration-200', expandedMenus.has(child.id) ? 'rotate-90' : '']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
              <div v-else class="w-6"></div>

              <div class="w-8 h-8 rounded-lg bg-surface-50 flex items-center justify-center shrink-0">
                <span class="text-xs font-medium text-surface-500">{{ child.name.charAt(0) }}</span>
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="text-sm text-surface-800">{{ child.name }}</span>
                  <span class="px-1.5 py-0.5 text-[10px] bg-surface-100 text-surface-500 rounded">{{ child.code }}</span>
                  <span :class="[
                    'px-1.5 py-0.5 text-[10px] rounded',
                    child.type === 'menu' ? 'bg-brand-50 text-brand-600' : 'bg-surface-50 text-surface-500'
                  ]">{{ child.type === 'menu' ? '菜单' : '按钮' }}</span>
                </div>
                <p class="text-xs text-surface-400 mt-0.5 truncate">{{ child.path || child.description || '-' }}</p>
              </div>

              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button 
                  v-if="child.type !== 'button'"
                  @click="addChildMenu(child)"
                  class="px-2.5 py-1.5 text-xs font-medium text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                >添加</button>
                <button 
                  @click="editMenu(child)"
                  class="px-2.5 py-1.5 text-xs font-medium text-surface-600 hover:bg-surface-100 rounded-lg transition-colors"
                >编辑</button>
                <button 
                  @click="deleteMenu(child.id)"
                  class="px-2.5 py-1.5 text-xs font-medium text-surface-400 hover:text-rose-500 hover:bg-rose-50 rounded-lg transition-colors"
                >删除</button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- 模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md animate-fade-in">
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-100">
          <h3 class="text-base font-semibold text-surface-900">{{ showEditModal ? '编辑菜单' : '添加菜单' }}</h3>
          <button @click="closeModal" class="w-8 h-8 rounded-lg hover:bg-surface-100 flex items-center justify-center transition-colors">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">菜单名称</label>
            <input 
              v-model="formData.name"
              type="text"
              required
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="如: 用户管理"
            />
          </div>
          
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">菜单代码</label>
            <input 
              v-model="formData.code"
              type="text"
              required
              :disabled="showEditModal"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white disabled:bg-surface-100 disabled:text-surface-400 transition-all"
              placeholder="如: system:user"
            />
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-surface-600 mb-1.5">类型</label>
              <select 
                v-model="formData.type"
                class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-700 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
              >
                <option value="directory">目录</option>
                <option value="menu">菜单</option>
                <option value="button">按钮</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium text-surface-600 mb-1.5">排序</label>
              <input 
                v-model.number="formData.sort_order"
                type="number"
                class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              />
            </div>
          </div>

          <div v-if="formData.type !== 'button'">
            <label class="block text-xs font-medium text-surface-600 mb-1.5">路由路径</label>
            <input 
              v-model="formData.path"
              type="text"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="如: /system/users"
            />
          </div>
          
          <div v-if="formData.type === 'menu'">
            <label class="block text-xs font-medium text-surface-600 mb-1.5">组件路径</label>
            <input 
              v-model="formData.component"
              type="text"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="如: system/users/index"
            />
          </div>

          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">图标</label>
            <input 
              v-model="formData.icon"
              type="text"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="如: Setting, User, Menu"
            />
          </div>
          
          <div>
            <label class="block text-xs font-medium text-surface-600 mb-1.5">描述</label>
            <textarea 
              v-model="formData.description"
              rows="2"
              class="w-full px-3.5 py-2.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all resize-none"
              placeholder="选填"
            ></textarea>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { menuApi } from '@/api/system/menu'
import type { Menu, MenuCreate, MenuUpdate } from '@/api/system/types'

const menuTree = ref<Menu[]>([])
const expandedMenus = ref(new Set<number>())
const showAddModal = ref(false)
const showEditModal = ref(false)
const loading = ref(false)
const editingMenuId = ref<number | null>(null)

const formData = reactive({
  name: '',
  code: '',
  type: 'menu' as string,
  path: '',
  component: '',
  icon: '',
  parent_id: null as number | null,
  sort_order: 0,
  description: ''
})

function toggleExpand(id: number) {
  if (expandedMenus.value.has(id)) {
    expandedMenus.value.delete(id)
  } else {
    expandedMenus.value.add(id)
  }
}

function addChildMenu(parent: Menu) {
  formData.parent_id = parent.id
  showAddModal.value = true
}

function editMenu(menu: Menu) {
  editingMenuId.value = menu.id
  formData.name = menu.name
  formData.code = menu.code
  formData.type = menu.type
  formData.path = menu.path || ''
  formData.component = menu.component || ''
  formData.icon = menu.icon || ''
  formData.parent_id = menu.parent_id || null
  formData.sort_order = menu.sort_order
  formData.description = menu.description || ''
  showEditModal.value = true
}

function closeModal() {
  showAddModal.value = false
  showEditModal.value = false
  editingMenuId.value = null
  resetForm()
}

function resetForm() {
  formData.name = ''
  formData.code = ''
  formData.type = 'menu'
  formData.path = ''
  formData.component = ''
  formData.icon = ''
  formData.parent_id = null
  formData.sort_order = 0
  formData.description = ''
}

async function handleSubmit() {
  loading.value = true
  try {
    if (showEditModal.value && editingMenuId.value) {
      const updateData: MenuUpdate = {
        name: formData.name,
        type: formData.type,
        path: formData.path || undefined,
        component: formData.component || undefined,
        icon: formData.icon || undefined,
        sort_order: formData.sort_order,
        description: formData.description || undefined
      }
      await menuApi.updateMenu(editingMenuId.value, updateData)
    } else {
      const createData: MenuCreate = {
        name: formData.name,
        code: formData.code,
        type: formData.type,
        path: formData.path || undefined,
        component: formData.component || undefined,
        icon: formData.icon || undefined,
        parent_id: formData.parent_id || undefined,
        sort_order: formData.sort_order,
        description: formData.description || undefined
      }
      await menuApi.createMenu(createData)
    }
    await fetchMenus()
    closeModal()
  } catch (error) {
    console.error('Failed to save menu:', error)
  } finally {
    loading.value = false
  }
}

async function deleteMenu(menuId: number) {
  if (!confirm('确定要删除这个菜单吗？')) return
  try {
    await menuApi.deleteMenu(menuId)
    await fetchMenus()
  } catch (error) {
    console.error('Failed to delete menu:', error)
  }
}

async function fetchMenus() {
  try {
    menuTree.value = await menuApi.getMenus()
  } catch (error) {
    console.error('Failed to fetch menus:', error)
  }
}

onMounted(() => {
  fetchMenus()
})
</script>
