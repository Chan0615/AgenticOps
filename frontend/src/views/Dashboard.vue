<template>
  <div>
    <!-- 标题区 -->
    <div class="mb-8">
      <h1 class="text-xl font-bold text-surface-900">知识库概览</h1>
      <p class="text-sm text-surface-400 mt-1">托马斯回旋喵 · 管理你的智能知识库</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div
        v-for="(card, i) in statCards"
        :key="i"
        class="bg-white rounded-2xl border border-surface-100 p-5 hover:border-brand-200 hover:shadow-lg hover:shadow-brand-100/50 transition-all duration-300"
      >
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs text-surface-400 mb-1">{{ card.label }}</p>
            <p class="text-2xl font-bold text-surface-900">{{ card.value }}</p>
          </div>
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center', card.bgClass]">
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
      <div class="lg:col-span-2 bg-white rounded-2xl border border-surface-100 p-6">
        <div class="flex items-center justify-between mb-5">
          <h3 class="text-sm font-semibold text-surface-900">最近更新的知识</h3>
          <button class="text-xs text-brand-500 hover:text-brand-600 transition-colors">查看全部</button>
        </div>
        <div class="space-y-1">
          <div
            v-for="item in recentDocs"
            :key="item.id"
            class="flex items-center gap-4 p-3 rounded-xl hover:bg-brand-50/50 transition-colors cursor-pointer group"
          >
            <div class="w-9 h-9 rounded-xl bg-surface-50 border border-surface-100 flex items-center justify-center shrink-0">
              <svg class="w-4 h-4 text-surface-400 group-hover:text-brand-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-surface-800 truncate group-hover:text-brand-600 transition-colors">{{ item.title }}</p>
              <p class="text-xs text-surface-400 mt-0.5">{{ item.category }} · {{ item.time }}</p>
            </div>
            <span class="text-[10px] px-2 py-0.5 rounded-full" :class="item.tagClass">{{ item.tag }}</span>
          </div>
        </div>
      </div>

      <!-- 托马斯回旋喵 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-6">
        <div class="flex items-center gap-3 mb-5">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-surface-900">托马斯回旋喵</h3>
            <p class="text-xs text-surface-400">AI 智能助手</p>
          </div>
        </div>
        <div class="bg-brand-50 rounded-xl p-4 mb-4">
          <p class="text-sm text-surface-700">你好！我是托马斯回旋喵，你的智能知识库助手。有什么问题可以随时问我 🐱</p>
        </div>
        <div class="relative">
          <input
            type="text"
            placeholder="问我任何问题..."
            class="w-full h-10 px-4 pr-10 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
          />
          <button class="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-lg bg-brand-500 hover:bg-brand-600 flex items-center justify-center transition-colors">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="bg-white rounded-2xl border border-surface-100 p-6">
      <h3 class="text-sm font-semibold text-surface-900 mb-5">快捷操作</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button
          v-for="action in quickActions"
          :key="action.label"
          class="flex items-center gap-3 p-4 rounded-xl border border-surface-100 hover:border-brand-200 hover:bg-brand-50/50 transition-all duration-200 group"
        >
          <div :class="['w-9 h-9 rounded-xl flex items-center justify-center', action.bgClass]">
            <svg class="w-4 h-4" :class="action.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.icon" />
            </svg>
          </div>
          <span class="text-sm text-surface-600 group-hover:text-brand-600 transition-colors">{{ action.label }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const recentDocs = [
  { id: 1, title: 'FastAPI 最佳实践与架构指南', category: '技术文档', time: '10 分钟前', tag: '已发布', tagClass: 'bg-emerald-50 text-emerald-600' },
  { id: 2, title: 'SQLAlchemy ORM 查询优化策略', category: '技术文档', time: '1 小时前', tag: '已发布', tagClass: 'bg-emerald-50 text-emerald-600' },
  { id: 3, title: 'Docker 容器化部署规范', category: '运维手册', time: '3 小时前', tag: '审核中', tagClass: 'bg-amber-50 text-amber-600' },
  { id: 4, title: 'Vue3 组件设计模式总结', category: '前端知识', time: '昨天', tag: '已发布', tagClass: 'bg-emerald-50 text-emerald-600' },
  { id: 5, title: 'Redis 缓存策略与常见问题', category: '技术文档', time: '2 天前', tag: '草稿', tagClass: 'bg-surface-100 text-surface-500' },
]

const statCards = [
  { label: '知识文档', value: '1,284', bgClass: 'bg-brand-50', iconClass: 'text-brand-500', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z', trend: '+24 本周新增', trendClass: 'text-brand-500' },
  { label: 'AI 问答次数', value: '3,672', bgClass: 'bg-pink-50', iconClass: 'text-pink-500', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z', trend: '+156 今日', trendClass: 'text-emerald-500' },
  { label: '活跃用户', value: '86', bgClass: 'bg-emerald-50', iconClass: 'text-emerald-500', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z', trend: '在线', trendClass: 'text-emerald-500' },
  { label: '知识分类', value: '42', bgClass: 'bg-amber-50', iconClass: 'text-amber-500', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10', trend: '已整理', trendClass: 'text-surface-400' },
]

const quickActions = [
  { label: '新建知识文档', bgClass: 'bg-brand-50', iconClass: 'text-brand-500', icon: 'M12 4v16m8-8H4' },
  { label: 'AI 智能问答', bgClass: 'bg-pink-50', iconClass: 'text-pink-500', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' },
  { label: '导入外部知识', bgClass: 'bg-emerald-50', iconClass: 'text-emerald-500', icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12' },
  { label: '管理用户权限', bgClass: 'bg-amber-50', iconClass: 'text-amber-500', icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' },
]
</script>
