<template>
  <div class="min-h-screen bg-surface-950 flex">
    <!-- 侧边栏 -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-40 flex flex-col w-64 bg-surface-900 border-r border-surface-700/50 transition-transform duration-300 lg:translate-x-0 lg:static',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 h-16 border-b border-surface-700/50 shrink-0">
        <div class="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h1 class="text-sm font-bold text-white tracking-wide">AgenticOps</h1>
          <p class="text-[10px] text-surface-400">智能知识库平台</p>
        </div>
      </div>

      <!-- 菜单 -->
      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        <p class="px-3 py-2 text-[10px] font-semibold text-surface-500 uppercase tracking-widest">导航</p>

        <template v-if="loading">
          <div v-for="i in 4" :key="i" class="h-9 rounded-lg bg-surface-800 animate-pulse mb-1"></div>
        </template>

        <template v-else>
          <router-link
            v-for="item in menuTree"
            :key="item.id"
            :to="item.path || '#'"
            class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-surface-300 hover:bg-surface-800 hover:text-white transition-all duration-200 group"
            active-class="bg-brand-600/15 text-brand-400 font-medium"
          >
            <component :is="getIcon(item.icon)" class="w-[18px] h-[18px] shrink-0 opacity-70 group-hover:opacity-100" />
            <span>{{ item.name }}</span>
          </router-link>

          <!-- 二级菜单（系统管理下的子项） -->
          <div v-for="parent in menuTree.filter(m => m.children?.length)" :key="'parent-' + parent.id">
            <button
              v-if="parent.children?.length"
              @click="toggleGroup(parent.id)"
              class="flex items-center justify-between w-full px-3 py-2.5 rounded-lg text-sm text-surface-300 hover:bg-surface-800 hover:text-white transition-all duration-200 mt-1"
            >
              <div class="flex items-center gap-3">
                <component :is="getIcon(parent.icon)" class="w-[18px] h-[18px] shrink-0 opacity-70" />
                <span>{{ parent.name }}</span>
              </div>
              <svg
                :class="['w-4 h-4 transition-transform duration-200', expandedGroups[parent.id] ? 'rotate-180' : '']"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-show="expandedGroups[parent.id]" class="ml-4 pl-3 border-l border-surface-700/50 space-y-0.5 mt-1">
              <router-link
                v-for="child in parent.children"
                :key="child.id"
                :to="child.path || '#'"
                class="flex items-center gap-3 px-3 py-2 rounded-md text-sm text-surface-400 hover:bg-surface-800 hover:text-white transition-all duration-200"
                active-class="bg-brand-600/15 text-brand-400 font-medium"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-surface-600 shrink-0 group-hover:bg-brand-400"></span>
                {{ child.name }}
              </router-link>
            </div>
          </div>
        </template>
      </nav>

      <!-- 底部用户 -->
      <div class="shrink-0 p-3 border-t border-surface-700/50">
        <div class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-surface-800 transition-colors cursor-pointer" @click="userMenuOpen = !userMenuOpen">
          <div class="w-8 h-8 rounded-full bg-brand-600/20 border border-brand-500/30 flex items-center justify-center">
            <span class="text-xs font-semibold text-brand-400">{{ userInitial }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">{{ authStore.user?.username }}</p>
            <p class="text-[10px] text-surface-500 truncate">{{ authStore.user?.is_superuser ? '管理员' : '用户' }}</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- 遮罩 -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 lg:hidden"
    ></div>

    <!-- 右侧 -->
    <div class="flex-1 flex flex-col min-h-screen min-w-0">
      <!-- 顶栏 -->
      <header class="h-16 shrink-0 bg-surface-900/80 backdrop-blur-md border-b border-surface-700/50 flex items-center justify-between px-6">
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden p-2 rounded-lg hover:bg-surface-800 text-surface-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div>
            <h2 class="text-sm font-semibold text-white">{{ currentTitle }}</h2>
            <p class="text-xs text-surface-500">智能知识库管理</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <!-- 搜索 -->
          <div class="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-surface-800 border border-surface-700/50 text-surface-400 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span class="text-xs">搜索知识库...</span>
            <kbd class="ml-4 px-1.5 py-0.5 text-[10px] bg-surface-700 rounded text-surface-400">⌘K</kbd>
          </div>

          <!-- 用户下拉 -->
          <div class="relative">
            <button @click.stop="userMenuOpen = !userMenuOpen" class="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-surface-800 transition-colors">
              <div class="w-7 h-7 rounded-full bg-brand-600/20 border border-brand-500/30 flex items-center justify-center">
                <span class="text-xs font-semibold text-brand-400">{{ userInitial }}</span>
              </div>
              <svg class="w-3.5 h-3.5 text-surface-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-if="userMenuOpen" @click.stop class="absolute right-0 mt-2 w-56 bg-surface-800 border border-surface-700 rounded-xl shadow-2xl py-1.5 z-50 animate-fade-in">
              <div class="px-4 py-3 border-b border-surface-700">
                <p class="text-sm font-medium text-white">{{ authStore.user?.full_name || authStore.user?.username }}</p>
                <p class="text-xs text-surface-400 mt-0.5">{{ authStore.user?.email }}</p>
              </div>
              <button @click="handleLogout" class="w-full flex items-center gap-2.5 px-4 py-2.5 text-sm text-rose-400 hover:bg-rose-500/10 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                退出登录
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- 内容区 -->
      <main class="flex-1 p-6 overflow-auto bg-surface-950">
        <div class="animate-fade-in">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { menuApi } from '@/api/system/menu'
import type { Menu } from '@/api/system/types'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const sidebarOpen = ref(false)
const userMenuOpen = ref(false)
const loading = ref(true)
const menuTree = ref<Menu[]>([])
const expandedGroups = reactive<Record<number, boolean>>({})

const userInitial = computed(() => authStore.user?.username?.charAt(0).toUpperCase() || 'U')

const currentTitle = computed(() => {
  const meta = route.meta as Record<string, any>
  return meta?.title || '知识库'
})

function toggleGroup(id: number) {
  expandedGroups[id] = !expandedGroups[id]
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

// 图标映射
function getIcon(iconName?: string) {
  const icons: Record<string, any> = {
    DataBoard: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z' })
    ]),
    Setting: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
    ]),
    User: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' })
    ]),
    UserFilled: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
    ]),
    Menu: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 6h16M4 10h16M4 14h16M4 18h16' })
    ]),
  }
  return icons[iconName || ''] || icons['Menu']
}

// 点击外部关闭
function handleClickOutside() {
  userMenuOpen.value = false
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  try {
    const data = await menuApi.getMyMenus()
    menuTree.value = data
    // 默认展开第一个有子菜单的分组
    const firstParent = menuTree.value.find(m => m.children?.length)
    if (firstParent) expandedGroups[firstParent.id] = true
  } catch (e) {
    console.error('加载菜单失败:', e)
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
