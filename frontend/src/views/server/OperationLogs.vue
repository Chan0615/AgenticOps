<template>
  <div class="operation-logs">
    <a-card title="操作日志" :bordered="false">
      <template #extra>
        <a-button @click="loadLogs">
          <template #icon><icon-refresh /></template>
          刷新
        </a-button>
      </template>

      <!-- 搜索栏 -->
      <a-form :model="{}" layout="inline" class="search-form">
        <a-form-item label="模块">
          <a-select
            v-model="filterModule"
            placeholder="全部模块"
            allow-clear
            style="width: 150px"
            @change="handleSearch"
          >
            <a-option value="认证模块">认证模块</a-option>
            <a-option value="用户管理">用户管理</a-option>
            <a-option value="角色管理">角色管理</a-option>
            <a-option value="菜单管理">菜单管理</a-option>
            <a-option value="服务器管理">服务器管理</a-option>
            <a-option value="知识库管理">知识库管理</a-option>
            <a-option value="AI对话">AI对话</a-option>
          </a-select>
        </a-form-item>
        <a-form-item label="用户">
          <a-input
            v-model="filterUsername"
            placeholder="用户名"
            allow-clear
            style="width: 150px"
            @press-enter="handleSearch"
          />
        </a-form-item>
        <a-form-item label="时间范围">
          <a-range-picker
            v-model="dateRange"
            style="width: 250px"
            @change="handleSearch"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">
            <template #icon><icon-search /></template>
            搜索
          </a-button>
        </a-form-item>
        <a-form-item>
          <a-button @click="resetFilter">
            <template #icon><icon-refresh /></template>
            重置
          </a-button>
        </a-form-item>
      </a-form>

      <!-- 日志列表 -->
      <a-table
        :columns="columns"
        :data="logList"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #status_code="{ record }">
          <a-tag v-if="record.status_code" :color="getStatusColor(record.status_code)">
            {{ record.status_code }}
          </a-tag>
          <span v-else>-</span>
        </template>
        <template #execution_time="{ record }">
          <span v-if="record.execution_time">{{ record.execution_time }}ms</span>
          <span v-else>-</span>
        </template>
        <template #created_at="{ record }">
          {{ formatTime(record.created_at) }}
        </template>
        <template #actions="{ record }">
          <a-button type="text" size="small" @click="showLogDetail(record)">
            <template #icon><icon-eye /></template>
            详情
          </a-button>
        </template>
      </a-table>
    </a-card>

    <!-- 日志详情对话框 -->
    <a-modal
      v-model:visible="detailVisible"
      title="操作日志详情"
      width="800px"
      :footer="false"
    >
      <a-descriptions v-if="currentLog" :column="2" bordered>
        <a-descriptions-item label="操作用户">
          {{ currentLog.username || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="操作模块">
          <a-tag color="arcoblue">{{ currentLog.module }}</a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="操作类型">
          {{ currentLog.action }}
        </a-descriptions-item>
        <a-descriptions-item label="操作描述">
          {{ currentLog.description || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="请求方法">
          <a-tag v-if="currentLog.method" :color="getMethodColor(currentLog.method)">
            {{ currentLog.method }}
          </a-tag>
          <span v-else>-</span>
        </a-descriptions-item>
        <a-descriptions-item label="请求路径">
          {{ currentLog.path || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="响应状态">
          <a-tag v-if="currentLog.status_code" :color="getStatusColor(currentLog.status_code)">
            {{ currentLog.status_code }}
          </a-tag>
          <span v-else>-</span>
        </a-descriptions-item>
        <a-descriptions-item label="执行时间">
          {{ currentLog.execution_time ? `${currentLog.execution_time}ms` : '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="IP 地址">
          {{ currentLog.ip_address || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="操作时间">
          {{ formatTime(currentLog.created_at) }}
        </a-descriptions-item>
        <a-descriptions-item label="请求参数" :span="2">
          <pre class="json-content">{{ formatJson(currentLog.request_params) }}</pre>
        </a-descriptions-item>
        <a-descriptions-item label="响应数据" :span="2">
          <pre class="json-content">{{ formatJson(currentLog.response_data) }}</pre>
        </a-descriptions-item>
        <a-descriptions-item v-if="currentLog.error_message" label="错误信息" :span="2">
          <a-alert type="error">
            {{ currentLog.error_message }}
          </a-alert>
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import {
  IconRefresh,
  IconSearch,
  IconEye,
} from '@arco-design/web-vue/es/icon'
import { getOperationLogs, type OperationLog } from '@/api/common/logs'

const loading = ref(false)
const logList = ref<OperationLog[]>([])
const detailVisible = ref(false)
const currentLog = ref<OperationLog | null>(null)

// 过滤条件
const filterModule = ref('')
const filterUsername = ref('')
const dateRange = ref<[string, string] | null>(null)

const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showTotal: true,
  showPageSize: true,
  pageSizeOptions: [10, 20, 50, 100],
})

const columns = [
  { title: '操作时间', slotName: 'created_at', width: 180 },
  { title: '用户', dataIndex: 'username', width: 120 },
  { title: '模块', dataIndex: 'module', width: 120 },
  { title: '操作', dataIndex: 'action', width: 150 },
  { title: '描述', dataIndex: 'description', ellipsis: true, tooltip: true },
  { title: '方法', slotName: 'method', width: 80 },
  { title: '状态', slotName: 'status_code', width: 80 },
  { title: '耗时', slotName: 'execution_time', width: 100 },
  { title: 'IP', dataIndex: 'ip_address', width: 140 },
  { title: '操作', slotName: 'actions', width: 100, fixed: 'right' },
]

onMounted(() => {
  loadLogs()
})

async function loadLogs() {
  loading.value = true
  try {
    const params: any = {
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize,
    }

    if (filterModule.value) {
      params.module = filterModule.value
    }
    if (filterUsername.value) {
      params.username = filterUsername.value
    }
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_time = dateRange.value[0]
      params.end_time = dateRange.value[1]
    }

    const data = await getOperationLogs(params)
    logList.value = data.items
    pagination.total = data.total
  } catch (error) {
    Message.error('加载操作日志失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.current = 1
  loadLogs()
}

function resetFilter() {
  filterModule.value = ''
  filterUsername.value = ''
  dateRange.value = null
  pagination.current = 1
  loadLogs()
}

function handlePageChange(page: number) {
  pagination.current = page
  loadLogs()
}

function handlePageSizeChange(pageSize: number) {
  pagination.pageSize = pageSize
  pagination.current = 1
  loadLogs()
}

function showLogDetail(log: OperationLog) {
  currentLog.value = log
  detailVisible.value = true
}

function formatTime(timeStr: string): string {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function formatJson(obj: any): string {
  if (!obj) return '-'
  try {
    return JSON.stringify(obj, null, 2)
  } catch {
    return String(obj)
  }
}

function getStatusColor(statusCode: number): string {
  if (statusCode < 300) return 'green'
  if (statusCode < 400) return 'orange'
  return 'red'
}

function getMethodColor(method: string): string {
  const colors: Record<string, string> = {
    GET: 'blue',
    POST: 'green',
    PUT: 'orange',
    DELETE: 'red',
    PATCH: 'purple',
  }
  return colors[method] || 'gray'
}
</script>

<style scoped>
.operation-logs {
  padding: 20px;
}

.search-form {
  margin-bottom: 16px;
  padding: 16px;
  background: #f7f8fa;
  border-radius: 4px;
}

.json-content {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Menlo, Monaco, "Courier New", monospace';
  font-size: 12px;
  max-height: 300px;
  overflow: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
}
</style>
