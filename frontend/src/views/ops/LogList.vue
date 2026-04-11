<template>
  <div class="log-page ant-illustration-page">
    <Card :bordered="false">
      <Space wrap style="margin-bottom: 16px">
        <RangePicker v-model:value="dateRange" show-time value-format="YYYY-MM-DD HH:mm:ss" style="width: 320px" />

        <Select v-model:value="searchParams.status" allow-clear placeholder="执行状态" style="width: 140px">
          <SelectOption value="pending">等待中</SelectOption>
          <SelectOption value="running">运行中</SelectOption>
          <SelectOption value="success">成功</SelectOption>
          <SelectOption value="failed">失败</SelectOption>
        </Select>

        <Input v-model:value="searchParams.task_name" placeholder="任务名称" allow-clear style="width: 180px" />
        <Input v-model:value="searchParams.server_keyword" placeholder="服务器IP/名称" allow-clear style="width: 190px" />

        <Button type="primary" @click="handleSearch">搜索</Button>
        <Button @click="handleReset">重置</Button>
      </Space>

      <Table :columns="columns" :data-source="logList" :loading="loading" :pagination="pagination" row-key="id" @change="handleTableChange">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'task_info'">{{ formatTask(record) }}</template>
          <template v-else-if="column.key === 'server_info'">{{ record.server_ip || '-' }}</template>
          <template v-else-if="column.key === 'status'">
            <Tag :color="getStatusColor(record.status)">{{ getStatusText(record.status) }}</Tag>
          </template>
          <template v-else-if="column.key === 'duration'">
            <span v-if="record.duration">{{ record.duration.toFixed(2) }}秒</span>
            <span v-else>-</span>
          </template>
          <template v-else-if="column.key === 'created_at'">{{ formatDateTime(record.created_at) }}</template>
          <template v-else-if="column.key === 'actions'">
            <Button type="link" @click="handleView(record)">查看详情</Button>
          </template>
        </template>
      </Table>
    </Card>

    <Modal v-model:open="detailVisible" title="执行日志详情" width="920px" :footer="null">
      <Descriptions :column="2" bordered>
        <DescriptionsItem label="任务">{{ formatTask(detailData) }}</DescriptionsItem>
        <DescriptionsItem label="服务器IP">{{ detailData.server_ip || '-' }}</DescriptionsItem>
        <DescriptionsItem label="执行状态">
          <Tag :color="getStatusColor(detailData.status)">{{ getStatusText(detailData.status) }}</Tag>
        </DescriptionsItem>
        <DescriptionsItem label="开始时间">{{ formatDateTime(detailData.started_at) }}</DescriptionsItem>
        <DescriptionsItem label="结束时间">{{ formatDateTime(detailData.finished_at) }}</DescriptionsItem>
        <DescriptionsItem label="执行时长">{{ detailData.duration ? `${detailData.duration.toFixed(2)}秒` : '-' }}</DescriptionsItem>
        <DescriptionsItem label="退出码">{{ detailData.exit_code ?? '-' }}</DescriptionsItem>
      </Descriptions>

      <Divider>执行命令</Divider>
      <pre class="command-content">{{ detailData.command || '-' }}</pre>

      <template v-if="detailData.output">
        <Divider>标准输出</Divider>
        <pre class="output-content">{{ detailData.output }}</pre>
      </template>

      <template v-if="detailData.error">
        <Divider>错误输出</Divider>
        <pre class="error-content">{{ detailData.error }}</pre>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  Button,
  Card,
  DatePicker,
  Descriptions,
  Divider,
  Input,
  Modal,
  Select,
  Space,
  Table,
  Tag,
  message,
} from 'ant-design-vue'
import { getExecutionLogDetail, getExecutionLogs } from '@/api/ops/log'
import { formatDateTime } from '@/utils/datetime'

const SelectOption = Select.Option
const RangePicker = DatePicker.RangePicker
const DescriptionsItem = Descriptions.Item

const route = useRoute()

interface ExecutionLog {
  id: number
  task_id?: number
  task_name?: string
  server_id?: number
  server_ip?: string
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

const searchParams = reactive({
  status: '',
  task_id: '',
  task_name: '',
  server_keyword: '',
  recent_days: '',
})

const dateRange = ref<[string, string] | undefined>(undefined)

const logList = ref<ExecutionLog[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
})

const columns = [
  { title: '任务', key: 'task_info', width: 240 },
  { title: '服务器IP', key: 'server_info', width: 180 },
  { title: '状态', key: 'status', width: 100 },
  { title: '命令', dataIndex: 'command', key: 'command' },
  { title: '执行时长', key: 'duration', width: 120 },
  { title: '创建时间', key: 'created_at', width: 180 },
  { title: '操作', key: 'actions', width: 120, fixed: 'right' as const },
]

const detailVisible = ref(false)
const detailData = ref<ExecutionLog>({} as ExecutionLog)

const loadLogs = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (searchParams.status) params.status = searchParams.status
    if (searchParams.task_id) params.task_id = Number(searchParams.task_id)
    if (searchParams.task_name) params.task_name = searchParams.task_name
    if (searchParams.server_keyword) params.server_keyword = searchParams.server_keyword
    if (searchParams.recent_days) params.recent_days = Number(searchParams.recent_days)
    if (dateRange.value && dateRange.value[0] && dateRange.value[1]) {
      params.start_time = dateRange.value[0]
      params.end_time = dateRange.value[1]
    }

    const res = await getExecutionLogs(params)
    logList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载日志列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.current = 1
  loadLogs()
}

const handleReset = () => {
  searchParams.status = ''
  searchParams.task_id = ''
  searchParams.task_name = ''
  searchParams.server_keyword = ''
  searchParams.recent_days = ''
  dateRange.value = undefined
  pagination.current = 1
  loadLogs()
}

const handleTableChange = (pageInfo: any) => {
  pagination.current = pageInfo.current
  pagination.pageSize = pageInfo.pageSize
  loadLogs()
}

const formatTask = (record: ExecutionLog) => {
  if (record.task_id && record.task_name) return `${record.task_name} · ID ${record.task_id}`
  if (record.task_name) return record.task_name
  if (record.task_id) return `任务 ID ${record.task_id}`
  return '-'
}

const handleView = async (record: ExecutionLog) => {
  await openDetailById(record.id)
}

const openDetailById = async (logId: number) => {
  try {
    detailData.value = await getExecutionLogDetail(logId)
    detailVisible.value = true
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载日志详情失败')
  }
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'default',
    running: 'blue',
    success: 'green',
    failed: 'red',
  }
  return colors[status] || 'default'
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
  const queryTaskId = route.query.task_id
  const queryTaskName = route.query.task_name
  const queryRecentDays = route.query.recent_days
  const queryLogId = route.query.log_id

  if (typeof queryTaskId === 'string' && queryTaskId.trim()) {
    searchParams.task_id = queryTaskId.trim()
  }
  if (typeof queryTaskName === 'string' && queryTaskName.trim()) {
    searchParams.task_name = queryTaskName.trim()
  }
  if (typeof queryRecentDays === 'string' && queryRecentDays.trim()) {
    searchParams.recent_days = queryRecentDays.trim()
  }

  loadLogs()

  if (typeof queryLogId === 'string' && queryLogId.trim()) {
    const parsed = Number(queryLogId.trim())
    if (!Number.isNaN(parsed) && parsed > 0) {
      openDetailById(parsed)
    }
  }
})
</script>

<style scoped>
.command-content,
.output-content,
.error-content {
  background: #f5f8ff;
  border: 1px solid #dbeafe;
  padding: 14px;
  border-radius: 10px;
  overflow-x: auto;
  font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  max-height: 300px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.error-content {
  background: #fff1f2;
  border-color: #fecdd3;
  color: #be123c;
}
</style>
