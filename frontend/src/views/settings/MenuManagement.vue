<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800">菜单管理</h2>
      <button 
        @click="showAddModal = true"
        class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        添加菜单
      </button>
    </div>

    <!-- 菜单列表 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="p-4">
        <div v-if="menuTree.length === 0" class="p-12 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">没有菜单</h3>
          <p class="mt-1 text-sm text-gray-500">开始添加第一个菜单吧。</p>
        </div>
        
        <div v-else class="space-y-2">
          <div 
            v-for="menu in menuTree" 
            :key="menu.id"
            class="border border-gray-200 rounded-lg overflow-hidden"
          >
            <div 
              class="flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center flex-1">
                <button 
                  v-if="menu.children && menu.children.length > 0"
                  @click="toggleExpand(menu.id)"
                  class="mr-2 p-1 hover:bg-gray-200 rounded"
                >
                  <svg 
                    :class="['w-4 h-4 transition-transform', expandedMenus.has(menu.id) ? 'rotate-90' : '']"
                    fill="none" stroke="currentColor" viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
                <div v-else class="w-6"></div>
                
                <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
                  <span class="text-purple-600 font-medium">{{ menu.name.charAt(0) }}</span>
                </div>
                
                <div class="flex-1">
                  <div class="flex items-center">
                    <span class="font-medium text-gray-800">{{ menu.name }}</span>
                    <span class="ml-2 px-2 py-0.5 text-xs bg-gray-200 text-gray-600 rounded">{{ menu.code }}</span>
                    <span 
                      :class="[
                        'ml-2 px-2 py-0.5 text-xs rounded',
                        menu.type === 'directory' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                      ]"
                    >
                      {{ menu.type === 'directory' ? '目录' : '菜单' }}
                    </span>
                  </div>
                  <div class="text-sm text-gray-500 mt-1">
                    路径: {{ menu.path || '-' }} | 组件: {{ menu.component || '-' }}
                  </div>
                </div>
              </div>
              
              <div class="flex items-center space-x-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    menu.status ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ menu.status ? '正常' : '禁用' }}
                </span>
                
                <div class="flex space-x-2">
                  <button 
                    @click="addChildMenu(menu.id)"
                    class="p-2 text-gray-500 hover:bg-gray-200 rounded-lg transition-colors"
                    title="添加子菜单"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                  </button>
                  <button 
                    @click="editMenu(menu)"
                    class="p-2 text-purple-600 hover:bg-purple-100 rounded-lg transition-colors"
                    title="编辑"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button 
                    @click="deleteMenu(menu.id)"
                    class="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                    title="删除"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 子菜单 -->
            <div v-if="expandedMenus.has(menu.id) && menu.children && menu.children.length > 0" class="border-t border-gray-200">
              <div 
                v-for="child in menu.children" 
                :key="child.id"
                class="flex items-center justify-between p-4 pl-16 bg-white hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
              >
                <div class="flex items-center flex-1">
                  <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                    <span class="text-blue-600 font-medium text-sm">{{ child.name.charAt(0) }}</span>
                  </div>
                  
                  <div class="flex-1">
                    <div class="flex items-center">
                      <span class="font-medium text-gray-700">{{ child.name }}</span>
                      <span class="ml-2 px-2 py-0.5 text-xs bg-gray-200 text-gray-600 rounded">{{ child.code }}</span>
                      <span class="ml-2 px-2 py-0.5 text-xs bg-yellow-100 text-yellow-800 rounded">
                        {{ child.type === 'button' ? '按钮' : '菜单' }}
                      </span>
                    </div>
                    <div class="text-sm text-gray-500 mt-1">
                      路径: {{ child.path || '-' }}
                    </div>
                  </div>
                </div>
                
                <div class="flex items-center space-x-4">
                  <span 
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      child.status ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ child.status ? '正常' : '禁用' }}
                  </span>
                  
                  <div class="flex space-x-2">
                    <button 
                      @click="editMenu(child)"
                      class="p-2 text-purple-600 hover:bg-purple-100 rounded-lg transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                    <button 
                      @click="deleteMenu(child.id)"
                      class="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑菜单模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 sticky top-0 bg-white">
          <h3 class="text-lg font-semibold text-gray-800">
            {{ showEditModal ? '编辑菜单' : (parentId ? '添加子菜单' : '添加菜单') }}
          </h3>
        </div>
        
        <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">菜单名称</label>
            <input 
              v-model="formData.name"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">菜单代码</label>
            <input 
              v-model="formData.code"
              type="text"
              required
              :disabled="showEditModal"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-100"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">类型</label>
            <select 
              v-model="formData.type"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="menu">菜单</option>
              <option value="directory">目录</option>
              <option value="button">按钮</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">路由路径</label>
            <input 
              v-model="formData.path"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="/example"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">组件路径</label>
            <input 
              v-model="formData.component"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="@/views/example.vue"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">图标</label>
            <input 
              v-model="formData.icon"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="IconName"
            />
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
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <textarea 
              v-model="formData.description"
              rows="2"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            ></textarea>
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
import { menuApi } from '@/api/system/menu'
import type { Menu, MenuCreate, MenuUpdate } from '@/api/system/types'

const menus = ref<Menu[]>([])
const menuTree = ref<Menu[]>([])
const expandedMenus = ref(new Set<number>())
const showAddModal = ref(false)
const showEditModal = ref(false)
const loading = ref(false)
const editingMenuId = ref<number | null>(null)
const parentId = ref<number | null>(null)

const formData = reactive({
  name: '',
  code: '',
  type: 'menu',
  path: '',
  component: '',
  icon: '',
  sort_order: 0,
  status: true,
  description: ''
})

function toggleExpand(menuId: number) {
  if (expandedMenus.value.has(menuId)) {
    expandedMenus.value.delete(menuId)
  } else {
    expandedMenus.value.add(menuId)
  }
}

function buildMenuTree(menus: Menu[]): Menu[] {
  const map = new Map<number, Menu>()
  const roots: Menu[] = []
  
  menus.forEach(menu => {
    map.set(menu.id, { ...menu, children: [] })
  })
  
  menus.forEach(menu => {
    const node = map.get(menu.id)!
    if (menu.parent_id && map.has(menu.parent_id)) {
      map.get(menu.parent_id)!.children!.push(node)
    } else {
      roots.push(node)
    }
  })
  
  return roots
}

function editMenu(menu: Menu) {
  editingMenuId.value = menu.id
  formData.name = menu.name
  formData.code = menu.code
  formData.type = menu.type
  formData.path = menu.path || ''
  formData.component = menu.component || ''
  formData.icon = menu.icon || ''
  formData.sort_order = menu.sort_order
  formData.status = menu.status
  formData.description = menu.description || ''
  showEditModal.value = true
}

function addChildMenu(parentMenuId: number) {
  parentId.value = parentMenuId
  showAddModal.value = true
}

function closeModal() {
  showAddModal.value = false
  showEditModal.value = false
  editingMenuId.value = null
  parentId.value = null
  resetForm()
}

function resetForm() {
  formData.name = ''
  formData.code = ''
  formData.type = 'menu'
  formData.path = ''
  formData.component = ''
  formData.icon = ''
  formData.sort_order = 0
  formData.status = true
  formData.description = ''
}

async function handleSubmit() {
  loading.value = true
  try {
    const data = {
      name: formData.name,
      code: formData.code,
      type: formData.type,
      path: formData.path || undefined,
      component: formData.component || undefined,
      icon: formData.icon || undefined,
      sort_order: formData.sort_order,
      description: formData.description || undefined
    }
    
    if (showEditModal.value && editingMenuId.value) {
      const updateData: MenuUpdate = {
        ...data,
        status: formData.status
      }
      await menuApi.updateMenu(editingMenuId.value, updateData)
    } else {
      const createData: MenuCreate = {
        ...data,
        parent_id: parentId.value || undefined
      }
      await menuApi.createMenu(createData)
    }
    await fetchMenus()
    closeModal()
  } catch (error) {
    console.error('Failed to save menu:', error)
    alert('保存失败，请稍后重试')
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
    alert('删除失败，请稍后重试')
  }
}

async function fetchMenus() {
  try {
    const allMenus = await menuApi.getAllMenus()
    menus.value = allMenus
    menuTree.value = buildMenuTree(allMenus)
  } catch (error) {
    console.error('Failed to fetch menus:', error)
  }
}

onMounted(() => {
  fetchMenus()
})
</script>
