<template>
  <div class="p-4 md:p-5 h-[calc(100vh-86px)] overflow-hidden bg-surface-50">
    <div class="h-full grid grid-rows-[auto_auto_1fr] gap-4">
      <section class="bg-white rounded-2xl border border-brand-100 px-5 py-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-brand-500">AGENTICOPS DASHBOARD</p>
            <h1 class="text-2xl font-bold text-surface-900 mt-1">运营概览</h1>
          </div>
          <div class="text-right">
            <p class="text-xs text-surface-400">{{ today }}</p>
            <p class="text-sm text-brand-600 mt-1">任务成功率 {{ successRate }}%</p>
          </div>
        </div>
      </section>

      <section class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-8 gap-3">
        <article v-for="kpi in kpis" :key="kpi.label" class="bg-white rounded-xl border border-surface-200 px-3 py-3">
          <p class="text-[11px] text-surface-400">{{ kpi.label }}</p>
          <p class="text-xl font-bold text-surface-900 mt-1">{{ kpi.value }}</p>
          <p class="text-[11px] mt-1" :class="kpi.hintClass">{{ kpi.hint }}</p>
        </article>
      </section>

      <section class="min-h-0 grid grid-rows-[auto_1fr] gap-4">
        <div class="bg-white rounded-2xl border border-surface-200 p-4">
          <h3 class="text-sm font-semibold text-surface-900">快捷入口</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 mt-3">
            <router-link to="/ops/tasks" class="quick-card">任务中心</router-link>
            <router-link to="/ops/logs" class="quick-card">执行日志</router-link>
            <router-link to="/rag/knowledge" class="quick-card">知识库管理</router-link>
            <router-link to="/ops/servers" class="quick-card">服务器列表</router-link>
          </div>
        </div>

        <div class="min-h-0 grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div class="bg-white rounded-2xl border border-surface-200 p-4 min-h-0 overflow-auto">
            <h3 class="text-sm font-semibold text-surface-900">系统公告</h3>
            <div class="space-y-2 mt-3">
              <div v-for="n in notices" :key="n.title" class="notice-row">
                <p class="text-sm text-surface-800">{{ n.title }}</p>
                <p class="text-xs text-surface-400 mt-0.5">{{ n.time }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-2xl border border-surface-200 p-4 min-h-0 overflow-auto">
            <h3 class="text-sm font-semibold text-surface-900">运行态势</h3>
            <div class="space-y-2 mt-3">
              <div v-for="item in health" :key="item.name" class="health-row">
                <div class="flex items-center justify-between">
                  <p class="text-sm text-surface-800">{{ item.name }}</p>
                  <span class="status-pill" :class="item.statusClass">{{ item.status }}</span>
                </div>
                <p class="text-xs text-surface-400 mt-0.5">{{ item.desc }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-2xl border border-surface-200 p-4 min-h-0 overflow-auto">
            <h3 class="text-sm font-semibold text-surface-900">系统脉冲</h3>
            <div class="space-y-2 mt-3">
              <div v-for="event in events" :key="event.title + event.time" class="pulse-row">
                <span class="w-2 h-2 rounded-full mt-1.5" :class="event.dotClass"></span>
                <div>
                  <p class="text-sm text-surface-800">{{ event.title }}</p>
                  <p class="text-xs text-surface-400 mt-0.5">{{ event.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

const now = new Date()
const today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`

const stats = ref({
  activeUsers: 9,
  docs: 24,
  indexedDocs: 20,
  servers: 18,
  todayRuns: 214,
  failedRuns: 6,
  chats: 15,
  chunks: 1560,
})

const successRate = computed(() => {
  if (!stats.value.todayRuns) return '100.0'
  return (((stats.value.todayRuns - stats.value.failedRuns) / stats.value.todayRuns) * 100).toFixed(1)
})

const kpis = computed(() => [
  { label: '活跃用户', value: stats.value.activeUsers, hint: '近 7 日', hintClass: 'text-brand-600' },
  { label: '知识文档', value: stats.value.docs, hint: `${stats.value.indexedDocs} 已索引`, hintClass: 'text-emerald-600' },
  { label: '运维主机', value: stats.value.servers, hint: '在线 16', hintClass: 'text-cyan-600' },
  { label: '今日会话', value: stats.value.chats, hint: 'AI 请求', hintClass: 'text-amber-600' },
  { label: '执行总量', value: stats.value.todayRuns, hint: '今日任务', hintClass: 'text-surface-500' },
  { label: '失败次数', value: stats.value.failedRuns, hint: '需关注', hintClass: 'text-rose-600' },
  { label: '向量片段', value: stats.value.chunks, hint: '检索基座', hintClass: 'text-fuchsia-600' },
  { label: '任务成功率', value: `${successRate.value}%`, hint: '稳定运行', hintClass: 'text-teal-600' },
])

const notices = ref([
  { title: '日志归档策略已开启（保留 90 天）', time: '今天 09:30' },
  { title: '请关注 2 台离线主机恢复', time: '今天 10:10' },
  { title: '夜间巡检任务已生效', time: '今天 11:00' },
])

const events = ref([
  { title: 'AI检测脚本执行失败', time: '12 分钟前', dotClass: 'bg-rose-500' },
  { title: '日志归档任务完成', time: '43 分钟前', dotClass: 'bg-emerald-500' },
  { title: '新增知识库文档', time: '2 小时前', dotClass: 'bg-amber-500' },
  { title: '主机连通性巡检', time: '3 小时前', dotClass: 'bg-cyan-500' },
])

const health = ref([
  { name: '计划任务调度', status: '正常', statusClass: 'ok', desc: '每分钟检查，无积压' },
  { name: 'Celery 队列', status: '可用', statusClass: 'good', desc: 'Worker 在线，平均延迟 < 2s' },
  { name: '日志存储', status: '关注', statusClass: 'warn', desc: '建议保持 90 天在线数据' },
])
</script>

<style scoped>
.quick-card {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 11px 8px;
  border-radius: 10px;
  border: 1px solid #fbcfe8;
  background: #fff1f7;
  color: #9d174d;
  font-size: 12px;
  font-weight: 600;
  transition: all .2s ease;
}

.quick-card:hover {
  border-color: #f472b6;
  background: #ffe4f1;
}

.notice-row,
.health-row,
.pulse-row {
  border: 1px solid #f1f5f9;
  border-radius: 10px;
  background: #fff;
  padding: 9px 10px;
}

.pulse-row {
  display: flex;
  gap: 9px;
  align-items: flex-start;
}

.status-pill {
  font-size: 11px;
  border-radius: 999px;
  padding: 2px 8px;
}

.status-pill.ok { background: #dcfce7; color: #166534; }
.status-pill.good { background: #e0f2fe; color: #075985; }
.status-pill.warn { background: #fef3c7; color: #92400e; }
</style>
