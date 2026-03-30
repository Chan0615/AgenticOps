<template>
  <div class="p-6">
    <!-- 页头 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900">仪表盘</h1>
      <p class="text-sm text-surface-400 mt-1">系统数据概览与统计</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <!-- 用户统计 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-5 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-surface-400 mb-1">总用户数</p>
            <p class="text-3xl font-bold text-surface-900">{{ stats.totalUsers }}</p>
            <p class="text-xs text-emerald-500 mt-1 flex items-center gap-1">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
              +{{ stats.newUsersToday }} 今日新增
            </p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-brand-50 flex items-center justify-center">
            <svg class="w-6 h-6 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 文档统计 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-5 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-surface-400 mb-1">知识库文档</p>
            <p class="text-3xl font-bold text-surface-900">{{ stats.totalDocs }}</p>
            <p class="text-xs text-emerald-500 mt-1 flex items-center gap-1">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
              {{ stats.indexedDocs }} 已索引
            </p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-cyan-50 flex items-center justify-center">
            <svg class="w-6 h-6 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 对话统计 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-5 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-surface-400 mb-1">今日对话</p>
            <p class="text-3xl font-bold text-surface-900">{{ stats.todayChats }}</p>
            <p class="text-xs text-surface-400 mt-1">累计 {{ stats.totalChats }} 次对话</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center">
            <svg class="w-6 h-6 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 向量片段 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-5 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-surface-400 mb-1">向量片段</p>
            <p class="text-3xl font-bold text-surface-900">{{ stats.totalChunks }}</p>
            <p class="text-xs text-surface-400 mt-1">用于语义检索</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center">
            <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷入口 -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-surface-900 mb-4">快捷入口</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <router-link 
          to="/rag/chat"
          class="group bg-gradient-to-br from-brand-500 to-brand-600 rounded-2xl p-6 text-white hover:shadow-xl hover:shadow-brand-200/50 transition-all"
        >
          <div class="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-1">AI 问答</h3>
          <p class="text-sm text-brand-100">基于 RAG 的智能知识问答</p>
        </router-link>

        <router-link 
          to="/rag/knowledge"
          class="group bg-white border border-surface-200 rounded-2xl p-6 hover:border-brand-300 hover:shadow-lg transition-all"
        >
          <div class="w-12 h-12 rounded-xl bg-cyan-50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-6 h-6 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-surface-900 mb-1">知识库管理</h3>
          <p class="text-sm text-surface-400">上传和管理知识文档</p>
        </router-link>

        <router-link 
          to="/settings/users"
          class="group bg-white border border-surface-200 rounded-2xl p-6 hover:border-brand-300 hover:shadow-lg transition-all"
        >
          <div class="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-6 h-6 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-surface-900 mb-1">系统设置</h3>
          <p class="text-sm text-surface-400">用户、角色、菜单管理</p>
        </router-link>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 最近对话 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-surface-900">最近对话</h3>
          <router-link to="/rag/chat" class="text-sm text-brand-600 hover:text-brand-700">查看全部</router-link>
        </div>
        <div class="space-y-3">
          <div v-for="(chat, i) in recentChats" :key="i" class="flex items-center gap-3 p-3 bg-surface-50 rounded-xl">
            <div class="w-10 h-10 rounded-lg bg-brand-100 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-surface-900 truncate">{{ chat.title }}</p>
              <p class="text-xs text-surface-400">{{ chat.time }}</p>
            </div>
          </div>
          <div v-if="recentChats.length === 0" class="text-center py-8 text-surface-400">
            暂无对话记录
          </div>
        </div>
      </div>

      <!-- 最近上传 -->
      <div class="bg-white rounded-2xl border border-surface-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-surface-900">最近上传</h3>
          <router-link to="/rag/knowledge" class="text-sm text-brand-600 hover:text-brand-700">查看全部</router-link>
        </div>
        <div class="space-y-3">
          <div v-for="(doc, i) in recentDocs" :key="i" class="flex items-center gap-3 p-3 bg-surface-50 rounded-xl">
            <div class="w-10 h-10 rounded-lg bg-cyan-100 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-surface-900 truncate">{{ doc.name }}</p>
              <p class="text-xs text-surface-400">{{ doc.size }} · {{ doc.time }}</p>
            </div>
            <span 
              class="text-xs px-2 py-1 rounded-full"
              :class="{
                'bg-emerald-50 text-emerald-600': doc.status === 'indexed',
                'bg-amber-50 text-amber-600': doc.status === 'pending'
              }"
            >
              {{ doc.status === 'indexed' ? '已索引' : '处理中' }}
            </span>
          </div>
          <div v-if="recentDocs.length === 0" class="text-center py-8 text-surface-400">
            暂无文档上传
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const stats = ref({
  totalUsers: 12,
  newUsersToday: 2,
  totalDocs: 24,
  indexedDocs: 20,
  todayChats: 15,
  totalChats: 128,
  totalChunks: 1560
})

const recentChats = ref([
  { title: 'FastAPI 异步数据库操作', time: '10分钟前' },
  { title: 'Vue3 Composition API 最佳实践', time: '1小时前' },
  { title: 'RAG 向量检索原理', time: '3小时前' },
])

const recentDocs = ref([
  { name: '项目架构设计.docx', size: '156 KB', time: '30分钟前', status: 'indexed' },
  { name: 'API 接口文档.md', size: '12 KB', time: '2小时前', status: 'indexed' },
  { name: '部署指南.pdf', size: '2.4 MB', time: '5小时前', status: 'pending' },
])
</script>
