<template>
  <div class="log-list-container">
    <a-card :bordered="false">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <a-space wrap>
          <a-range-picker
            v-model="dateRange"
            style="width: 250px"
          />
          
          <a-select
            v-model="searchParams.status"
            placeholder="执行状态"
            allow-clear
            style="width: 150px"
          >
            <a-option value="pending">等待中</a-option>
            <a-option value="running">运行中</a-option>
            <a-option value="success">成功</a-option>
            <a-option value="failed">失败</a-option>
          </a-select>
          
          <a-input
            v-model="searchParams.task_id"
            placeholder="任务ID"
            allow-clear
            style="width: 120px"
          />
          
          <a-button type="primary" @click="handleSearch">
            <template #icon><icon-search /></template>
            搜索
          </a-button>
          
          <a-button @click="handleReset">
            <template #icon><icon-refresh /></template>
            重置
          </a-button>
        </a-space>
      </div>

      <!-- 表格 -->
      <a-table
        :columns="columns"
        :data="logList"
        :loading="loading"
        :pagination="pagination"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #status="{ record }">
          <a-tag :color="getStatusColor(record.status)">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>
        
        <template #duration="{ record }">
          <span v-if="record.duration">
            {{ record.duration.toFixed(2) }}秒
          </span>
          <span v-else>-</span>
        </template>
        
        <template #actions="{ record }">
          <a-button type="text" size="small" @click="handleView(record)">
            查看详情
          </a-button>
        </template>
      </a-table>
    </a-card>

    <!-- 详情对话框 -->
    <a-modal
      v-model:visible="detailVisible"
      title="执行日志详情"
      width="900px"
      :footer="false"
    >
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="日志ID">
          {{ detailData.id }}
        </a-descriptions-item>
        <a-descriptions-item label="任务ID">
          {{ detailData.task_id || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="服务器ID">
          {{ detailData.server_id || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="执行状态">
          <a-tag :color="getStatusColor(detailData.status)">
            {{ getStatusText(detailData.status) }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="开始时间">
          {{ detailData.started_at || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="结束时间">
          {{ detailData.finished_at || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="执行时长">
          {{ detailData.duration ? detailData.duration.toFixed(2) + '秒' : '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="退出码">
          {{ detailData.exit_code ?? '-' }}
        </a-descriptions-item>
      </a-descriptions>
      
      <a-divider>执行命令</a-divider>
      <pre class="command-content">{{ detailData.command || '-' }}</pre>
      
      <a-divider v-if="detailData.output">标准输出</a-divider>
      <pre v-if="detailData.output" class="output-content">{{ detailData.output }}</pre>
      
      <a-divider v-if="detailData.error" status="danger">错误输出</a-divider>
      <pre v-if="detailData.error" class="error-content">{{ detailData.error }}</pre>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import {
  IconSearch,
  IconRefresh,
} from '@arco-design/web-vue/es/icon'
import { getExecutionLogs, getExecutionLogDetail } from '@/api/ops/log'

interface ExecutionLog {
  id: number
  task_id?: number
  server_id?: number
  status: string
  command: string
  output?: string
  error?: string
  exit_code?: number
  started_at?: string
  finished_at?: string
  duration?: number
  created_at: string
}

// 搜索参数
const searchParams = reactive({
  status: '',
  task_id: '',
})

const dateRange = ref<[string, string] | undefined>()

// 表格数据
const logList = ref<ExecutionLog[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showTotal: true,
  showPageSize: true,
})

// 表格列定义
const columns = [
  { title: 'ID', dataIndex: 'id', width: 80 },
  { title: '任务ID', dataIndex: 'task_id', width: 100 },
  { title: '服务器ID', dataIndex: 'server_id', width: 100 },
  { title: '状态', slotName: 'status', width: 100 },
  { title: '命令', dataIndex: 'command', ellipsis: true, tooltip: true },
  { title: '执行时长', slotName: 'duration', width: 120 },
  { title: '创建时间', dataIndex: 'created_at', width: 180 },
  { title: '操作', slotName: 'actions', width: 120, fixed: 'right' },
]

// 详情
const detailVisible = ref(false)
const detailData = ref<ExecutionLog>({} as ExecutionLog)

// 加载日志列表
const loadLogs = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (searchParams.status) params.status = searchParams.status
    if (searchParams.task_id) params.task_id = Number(searchParams.task_id)
    if (dateRange.value && dateRange.value[0] && dateRange.value[1]) {
      params.start_time = dateRange.value[0]
      params.end_time = dateRange.value[1]
    }

    const res = await getExecutionLogs(params)
    logList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '加载日志列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadLogs()
}

// 重置
const handleReset = () => {
  searchParams.status = ''
  searchParams.task_id = ''
  dateRange.value = undefined
  pagination.current = 1
  loadLogs()
}

// 分页
const handlePageChange = (page: number) => {
  pagination.current = page
  loadLogs()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize
  pagination.current = 1
  loadLogs()
}

// 查看详情
const handleView = async (record: ExecutionLog) => {
  try {
    const detail = await getExecutionLogDetail(record.id)
    detailData.value = detail
    detailVisible.value = true
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '加载日志详情失败')
  }
}

// 状态颜色
const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'gray',
    running: 'blue',
    success: 'green',
    failed: 'red',
  }
  return colors[status] || 'gray'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '等待中',
    running: '运行中',
    success: '成功',
    failed: '失败',
  }
  return texts[status] || status
}

onMounted(() => {
  loadLogs()
})
</script>

<style scoped>
.log-list-container {
  padding: 20px;
}

.search-bar {
  margin-bottom: 16px;
}

.command-content,
.output-content,
.error-content {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  max-height: 300px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.error-content {
  background: #fff1f0;
  color: #cf1322;
}
</style>
