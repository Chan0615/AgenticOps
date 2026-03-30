<template>
  <div>
    <!-- 标题区 -->
    <div class="mb-8">
      <h1 class="text-xl font-bold text-white">知识库概览</h1>
      <p class="text-sm text-surface-400 mt-1">管理和监控你的智能知识库系统</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div
        v-for="(card, i) in statCards"
        :key="i"
        class="card p-5 hover:border-brand-500/30 transition-all duration-300 group"
      >
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs text-surface-400 mb-1">{{ card.label }}</p>
            <p class="text-2xl font-bold text-white">{{ card.value }}</p>
          </div>
          <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', card.bgClass]">
            <svg class="w-5 h-5" :class="card.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="card.icon" />
            </svg>
          </div>
        </div>
        <p class="text-xs mt-3" :class="card.trendClass">{{ card.trend }}</p>
      </div>
    </div>

    <!-- 内容区 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- 最近知识 -->
      <div class="lg:col-span-2 card p-6">
        <div class="flex items-center justify-between mb-5">
          <h3 class="text-sm font-semibold text-white">最近更新的知识</h3>
          <button class="text-xs text-brand-400 hover:text-brand-300 transition-colors">查看全部</button>
        </div>
        <div class="space-y-3">
          <div
            v-for="item in recentDocs"
            :key="item.id"
            class="flex items-center gap-4 p-3 rounded-lg hover:bg-surface-700/30 transition-colors cursor-pointer group"
          >
            <div class="w-9 h-9 rounded-lg bg-surface-800 border border-surface-700/50 flex items-center justify-center shrink-0">
              <svg class="w-4 h-4 text-surface-400 group-hover:text-brand-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-surface-200 truncate group-hover:text-white transition-colors">{{ item.title }}</p>
              <p class="text-xs text-surface-500 mt-0.5">{{ item.category }} · {{ item.time }}</p>
            </div>
            <span class="text-[10px] px-2 py-0.5 rounded-full" :class="item.tagClass">{{ item.tag }}</span>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="card p-6">
        <h3 class="text-sm font-semibold text-white mb-5">快捷操作</h3>
        <div class="space-y-2">
          <button
            v-for="action in quickActions"
            :key="action.label"
            class="w-full flex items-center gap-3 p-3 rounded-lg border border-surface-700/50 hover:border-brand-500/30 hover:bg-brand-500/5 transition-all duration-200 group"
          >
            <div :class="['w-8 h-8 rounded-lg flex items-center justify-center', action.bgClass]">
              <svg class="w-4 h-4" :class="action.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.icon" />
              </svg>
            </div>
            <span class="text-sm text-surface-300 group-hover:text-white transition-colors">{{ action.label }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 底部状态 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="status in systemStatus"
        :key="status.label"
        class="card p-4 flex items-center gap-4"
      >
        <div :class="['w-2 h-2 rounded-full shrink-0', status.dotClass]"></div>
        <div class="flex-1">
          <p class="text-xs text-surface-400">{{ status.label }}</p>
          <p class="text-sm font-medium text-white mt-0.5">{{ status.value }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userApi } from '@/api/system/user'
import { roleApi } from '@/api/system/role'
import { menuApi } from '@/api/system/menu'

const stats = ref({ totalUsers: 0, activeRoles: 0, totalMenus: 0 })

const statCards = [
  { label: '知识文档', value: '1,284', bgClass: 'bg-brand-500/10', iconClass: 'text-brand-400', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z', trend: '+24 本周新增', trendClass: 'text-emerald-400' },
  { label: 'AI 问答次数', value: '3,672', bgClass: 'bg-cyan-500/10', iconClass: 'text-cyan-400', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z', trend: '+156 今日', trendClass: 'text-emerald-400' },
  { label: '活跃用户', value: '86', bgClass: 'bg-emerald-500/10', iconClass: 'text-emerald-400', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z', trend: '在线', trendClass: 'text-emerald-400' },
  { label: '知识分类', value: '42', bgClass: 'bg-amber-500/10', iconClass: 'text-amber-400', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10', trend: '已整理', trendClass: 'text-surface-400' },
]

const recentDocs = [
  { id: 1, title: 'FastAPI 最佳实践与架构指南', category: '技术文档', time: '10 分钟前', tag: '已发布', tagClass: 'bg-emerald-500/10 text-emerald-400' },
  { id: 2, title: 'SQLAlchemy ORM 查询优化策略', category: '技术文档', time: '1 小时前', tag: '已发布', tagClass: 'bg-emerald-500/10 text-emerald-400' },
  { id: 3, title: 'Docker 容器化部署规范', category: '运维手册', time: '3 小时前', tag: '审核中', tagClass: 'bg-amber-500/10 text-amber-400' },
  { id: 4, title: 'Vue3 组件设计模式总结', category: '前端知识', time: '昨天', tag: '已发布', tagClass: 'bg-emerald-500/10 text-emerald-400' },
  { id: 5, title: 'Redis 缓存策略与常见问题', category: '技术文档', time: '2 天前', tag: '草稿', tagClass: 'bg-surface-600/50 text-surface-400' },
]

const quickActions = [
  { label: '新建知识文档', bgClass: 'bg-brand-500/10', iconClass: 'text-brand-400', icon: 'M12 4v16m8-8H4' },
  { label: 'AI 智能问答', bgClass: 'bg-cyan-500/10', iconClass: 'text-cyan-400', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' },
  { label: '导入外部知识', bgClass: 'bg-emerald-500/10', iconClass: 'text-emerald-400', icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12' },
  { label: '管理用户权限', bgClass: 'bg-amber-500/10', iconClass: 'text-amber-400', icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' },
]

const systemStatus = [
  { label: '知识检索引擎', value: '运行正常', dotClass: 'bg-emerald-400' },
  { label: 'AI 模型服务', value: '已连接', dotClass: 'bg-emerald-400' },
  { label: '向量数据库', value: '同步中', dotClass: 'bg-amber-400' },
]

onMounted(async () => {
  try {
    const [users, roles, menus] = await Promise.all([
      userApi.getUsers().catch(() => []),
      roleApi.getRoles().catch(() => []),
      menuApi.getMenus().catch(() => []),
    ])
    stats.value.totalUsers = users.length
    stats.value.activeRoles = roles.filter((r: any) => r.status).length
    stats.value.totalMenus = menus.length
  } catch (e) {
    console.error('Failed to fetch stats:', e)
  }
})
</script>
