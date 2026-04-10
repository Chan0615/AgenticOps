<template>
  <div class="task-list-container">
    <a-card :bordered="false">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <a-space>
          <a-input
            v-model="searchParams.name"
            placeholder="搜索任务名称"
            allow-clear
            style="width: 200px"
            @press-enter="handleSearch"
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
          
          <a-select
            v-model="searchParams.enabled"
            placeholder="状态"
            allow-clear
            style="width: 120px"
          >
            <a-option :value="true">启用</a-option>
            <a-option :value="false">禁用</a-option>
          </a-select>
          
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

      <!-- 操作栏 -->
      <div class="action-bar">
        <a-button type="primary" @click="handleAdd">
          <template #icon><icon-plus /></template>
          创建任务
        </a-button>
      </div>

      <!-- 表格 -->
      <a-table
        :columns="columns"
        :data="taskList"
        :loading="loading"
        :pagination="pagination"
        :scroll="{ x: 'max-content' }"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #enabled="{ record }">
          <a-tag :color="record.enabled ? 'green' : 'red'">
            {{ record.enabled ? '已启用' : '已禁用' }}
          </a-tag>
        </template>
        
        <template #task_type="{ record }">
          <a-tag color="purple">SaltStack</a-tag>
        </template>

        <template #script_info="{ record }">
          <span v-if="record.script_id">
            {{ scriptNameMap[record.script_id] || `脚本#${record.script_id}` }}
          </span>
          <span v-else-if="record.command">内联命令</span>
          <span v-else>-</span>
        </template>

        <template #run_status="{ record }">
          <a-tag :color="getRunStatusColor(record)">
            {{ getRunStatusText(record) }}
          </a-tag>
        </template>

        <template #last_run_at="{ record }">
          {{ formatDateTime(record.last_run_at) }}
        </template>

        <template #next_run_at="{ record }">
          {{ formatDateTime(record.next_run_at) }}
        </template>

        <template #created_at="{ record }">
          {{ formatDateTime(record.created_at) }}
        </template>

        <template #targets="{ record }">
          <a-space wrap size="mini">
            <a-tag
              v-for="target in getTaskTargets(record).slice(0, 2)"
              :key="`${record.id}-${target.id}`"
              color="arcoblue"
            >
              {{ target.envText }} / {{ target.name }}
            </a-tag>
            <a-tag v-if="getTaskTargets(record).length > 2" color="gray">
              +{{ getTaskTargets(record).length - 2 }}
            </a-tag>
          </a-space>
        </template>
        
        <template #actions="{ record }">
          <a-space>
            <a-tag color="purple" :hoverable="true" @click="handleShowDetail(record)">
              详情
            </a-tag>
            <a-tag color="blue" :hoverable="true" @click="handleTrigger(record)">
              测试
            </a-tag>
            <a-tag color="arcoblue" :hoverable="true" @click="handleViewLogs(record)">
              日志
            </a-tag>
            <a-tag :hoverable="true" @click="handleEdit(record)">
              编辑
            </a-tag>
            <a-popconfirm content="确定要删除该任务吗？" @ok="handleDelete(record.id)">
              <a-tag color="red" :hoverable="true">
                删除
              </a-tag>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 添加/编辑对话框 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      width="800px"
      @ok="handleSubmit"
      @cancel="handleCancel"
    >
      <a-form :model="formData" layout="vertical">
        <a-form-item label="任务名称" required>
          <a-input v-model="formData.name" placeholder="例如：每日日志清理" />
        </a-form-item>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="执行方式" required>
              <a-select v-model="formData.task_type" disabled>
                <a-option value="salt">SaltStack</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="Cron表达式" required>
              <a-input
                v-model="formData.cron_expression"
                placeholder="例如：0 2 * * *"
              >
                <template #suffix>
                  <a-tooltip content="分 时 日 月 周">
                    <icon-question-circle />
                  </a-tooltip>
                </template>
              </a-input>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item v-if="isEdit" label="任务状态">
          <a-radio-group
            :model-value="formData.enabled"
            type="button"
            @change="(val: string | number | boolean) => (formData.enabled = val === true)"
          >
            <a-radio :value="true">启用</a-radio>
            <a-radio :value="false">禁用</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item v-if="formData.task_type === 'salt'" label="Salt 环境" required>
          <a-select
            v-model="selectedEnvironment"
            placeholder="选择环境后加载该环境服务器"
            allow-clear
            @change="formData.server_ids = []"
          >
            <a-option v-for="env in environmentOptions" :key="env.value" :value="env.value">
              {{ env.label }}
            </a-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="目标服务器" required>
          <a-select
            v-model="formData.server_ids"
            multiple
            :loading="loadingServers"
            :disabled="formData.task_type === 'salt' && !selectedEnvironment"
            :placeholder="formData.task_type === 'salt' && !selectedEnvironment ? '请先选择 Salt 环境' : '选择目标服务器'"
          >
            <a-option v-for="server in filteredServerOptions" :key="server.id" :value="server.id">
              {{ server.name }} ({{ server.hostname }})
            </a-option>
          </a-select>
        </a-form-item>

        <a-form-item label="执行脚本（可选）">
          <a-select
            v-model="formData.script_id"
            allow-clear
            placeholder="选择已上传脚本（不选则使用下方执行命令）"
          >
            <a-option v-for="script in scriptOptions" :key="script.id" :value="script.id">
              {{ script.name }}
            </a-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="执行命令">
          <a-textarea
            v-model="formData.command"
            :auto-size="{ minRows: 4, maxRows: 8 }"
            placeholder="输入要执行的命令..."
            style="font-family: monospace"
          />
        </a-form-item>
        
        <a-form-item label="描述">
          <a-textarea
            v-model="formData.description"
            :auto-size="{ minRows: 2, maxRows: 4 }"
            placeholder="任务描述信息"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal
      v-model:visible="detailVisible"
      title="任务详情"
      width="760px"
      :footer="false"
    >
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="任务名称">{{ detailData?.name || '-' }}</a-descriptions-item>
        <a-descriptions-item label="执行方式">SaltStack</a-descriptions-item>
        <a-descriptions-item label="脚本">
          <span v-if="detailData?.script_id">{{ scriptNameMap[detailData.script_id] || `脚本#${detailData.script_id}` }}</span>
          <span v-else-if="detailData?.command">内联命令</span>
          <span v-else>-</span>
        </a-descriptions-item>
        <a-descriptions-item label="状态">
          <a-tag :color="detailData?.enabled ? 'green' : 'red'">{{ detailData?.enabled ? '已启用' : '已禁用' }}</a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="Cron表达式">{{ detailData?.cron_expression || '-' }}</a-descriptions-item>
        <a-descriptions-item label="执行态">
          {{ detailData ? getRunStatusText(detailData) : '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="创建人">{{ detailData?.created_by || '-' }}</a-descriptions-item>
        <a-descriptions-item label="修改人">{{ detailData?.updated_by || '-' }}</a-descriptions-item>
        <a-descriptions-item label="创建时间">{{ formatDateTime(detailData?.created_at) }}</a-descriptions-item>
        <a-descriptions-item label="更新时间">{{ formatDateTime(detailData?.updated_at) }}</a-descriptions-item>
        <a-descriptions-item label="上次执行">{{ formatDateTime(detailData?.last_run_at) }}</a-descriptions-item>
        <a-descriptions-item label="下次执行">{{ formatDateTime(detailData?.next_run_at) }}</a-descriptions-item>
        <a-descriptions-item label="目标主机" :span="2">
          <a-space wrap>
            <a-tag v-for="target in detailTargets" :key="target.id" color="arcoblue">
              {{ target.envText }} / {{ target.name }}
            </a-tag>
          </a-space>
        </a-descriptions-item>
        <a-descriptions-item label="描述" :span="2">{{ detailData?.description || '-' }}</a-descriptions-item>
        <a-descriptions-item label="执行命令" :span="2">
          <pre class="task-command-pre">{{ detailData?.command || '-' }}</pre>
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import {
  IconSearch,
  IconRefresh,
  IconPlus,
  IconQuestionCircle,
} from '@arco-design/web-vue/es/icon'
import { getTaskList, getTaskDetail, createTask, updateTask, toggleTask, triggerTask, deleteTask } from '@/api/ops/task'
import { getServerList, type Server } from '@/api/ops/server'
import { getScriptList } from '@/api/ops/script'
import { formatDateTime } from '@/utils/datetime'

const router = useRouter()

interface Task {
  id: number
  name: string
  description?: string
  script_id?: number
  server_ids: number[]
  cron_expression: string
  task_type: 'salt'
  command?: string
  enabled: boolean
  celery_task_id?: string
  last_run_at?: string
  next_run_at?: string
  created_by?: string
  updated_by?: string
  created_at: string
  updated_at: string
}

interface TaskServerOption {
  id: number
  name: string
  hostname: string
  environment: string
}

// 搜索参数
const searchParams = reactive({
  name: '',
  enabled: undefined as boolean | undefined,
})

// 表格数据
const taskList = ref<Task[]>([])
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
  { title: '任务', dataIndex: 'name' },
  { title: '脚本', slotName: 'script_info' },
  { title: '执行态', slotName: 'run_status' },
  { title: '上次执行', slotName: 'last_run_at' },
  { title: '下次执行', slotName: 'next_run_at' },
  { title: '目标主机', slotName: 'targets' },
  { title: 'Cron', dataIndex: 'cron_expression' },
  { title: '状态', slotName: 'enabled' },
  { title: '创建时间', slotName: 'created_at' },
  { title: '操作', slotName: 'actions', width: 230, fixed: 'right' },
]

// 模态框
const modalVisible = ref(false)
const modalTitle = ref('创建任务')
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const detailVisible = ref(false)
const detailData = ref<Task | null>(null)

const formData = reactive<Partial<Task>>({
  name: '',
  task_type: 'salt',
  cron_expression: '',
  server_ids: [],
  command: '',
  enabled: true,
  description: '',
})

const serverOptions = ref<TaskServerOption[]>([])
const loadingServers = ref(false)
const selectedEnvironment = ref('')
const scriptNameMap = reactive<Record<number, string>>({})
const scriptOptions = ref<Array<{ id: number; name: string }>>([])

const environmentOptions = [
  { label: '富春云', value: 'fuchunyun' },
  { label: '阿里云', value: 'aliyun' },
  { label: '滨江', value: 'binjiang' },
  { label: '阿里云压测', value: 'aliyunyc' },
]

const envTextMap: Record<string, string> = {
  fuchunyun: '富春云',
  aliyun: '阿里云',
  binjiang: '滨江',
  aliyunyc: '阿里云压测',
}

const filteredServerOptions = computed(() => {
  if (formData.task_type !== 'salt') return serverOptions.value
  if (!selectedEnvironment.value) return []
  return serverOptions.value.filter(s => s.environment === selectedEnvironment.value)
})

const getTaskTargets = (task: Task) => {
  return (task.server_ids || []).map((id) => {
    const server = serverOptions.value.find((s) => s.id === id)
    if (!server) {
      return {
        id,
        name: `主机#${id}`,
        envText: '未知环境',
      }
    }
    return {
      id,
      name: server.name,
      envText: envTextMap[server.environment] || server.environment,
    }
  })
}

const detailTargets = computed(() => {
  if (!detailData.value) return []
  return getTaskTargets(detailData.value)
})

const getRunStatusText = (task: Task) => {
  if (!task.enabled) return '已停用'
  if (task.last_run_at) return '已执行'
  return '待执行'
}

const getRunStatusColor = (task: Task) => {
  if (!task.enabled) return 'gray'
  if (task.last_run_at) return 'green'
  return 'orange'
}

const loadServerOptions = async () => {
  loadingServers.value = true
  try {
    const pageSize = 100
    let page = 1
    let total = 0
    const allServers: Server[] = []

    do {
      const res = await getServerList({ page, page_size: pageSize })
      const items = res.data || []
      total = res.total || items.length
      allServers.push(...items)
      page += 1
    } while (allServers.length < total)

    serverOptions.value = allServers.map((s: Server) => ({
      id: s.id,
      name: s.name,
      hostname: s.hostname,
      environment: s.environment,
    }))
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '加载服务器列表失败')
    serverOptions.value = []
  } finally {
    loadingServers.value = false
  }
}

const loadScriptOptions = async () => {
  try {
    const pageSize = 100
    let page = 1
    const allScripts: Array<{ id: number; name: string }> = []

    while (true) {
      const res = await getScriptList({ page, page_size: pageSize })
      const items = res.data || []
      items.forEach((s) => {
        scriptNameMap[s.id] = s.name
        allScripts.push({ id: s.id, name: s.name })
      })
      if (!items.length || items.length < pageSize) break
      page += 1
    }
    scriptOptions.value = allScripts
  } catch (error) {
    console.error('加载脚本列表失败:', error)
    scriptOptions.value = []
  }
}

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (searchParams.name) params.name = searchParams.name
    if (typeof searchParams.enabled === 'boolean') params.enabled = searchParams.enabled

    const res = await getTaskList(params)
    taskList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    console.error('加载任务列表失败:', error)
    if (error.response && error.response.status !== 401) {
      Message.error('加载任务列表失败: ' + (error.response?.data?.detail || error.message))
    }
    taskList.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadTasks()
}

// 重置
const handleReset = () => {
  searchParams.name = ''
  searchParams.enabled = undefined
  pagination.current = 1
  loadTasks()
}

// 分页
const handlePageChange = (page: number) => {
  pagination.current = page
  loadTasks()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize
  pagination.current = 1
  loadTasks()
}

// 添加
const handleAdd = () => {
  isEdit.value = false
  modalTitle.value = '创建任务'
  resetForm()
  modalVisible.value = true
  loadServerOptions()
}

// 编辑
const handleEdit = async (record: Task) => {
  isEdit.value = true
  editingId.value = record.id
  modalTitle.value = '编辑任务'
  await loadServerOptions()
  Object.assign(formData, record)
  if (record.task_type === 'salt' && record.server_ids?.length) {
    const envSet = new Set(
      record.server_ids
        .map(id => serverOptions.value.find(s => s.id === id)?.environment)
        .filter((v): v is string => !!v)
    )
    selectedEnvironment.value = envSet.size === 1 ? Array.from(envSet)[0] : ''
  } else {
    selectedEnvironment.value = ''
  }
  modalVisible.value = true
}

// 切换状态
const handleToggle = async (record: Task) => {
  try {
    await toggleTask(record.id)
    Message.success(record.enabled ? '任务已启用' : '任务已禁用')
    loadTasks()
  } catch (error) {
    Message.error('操作失败')
    record.enabled = !record.enabled
  }
}

// 手动触发
const handleTrigger = async (record: Task) => {
  try {
    await triggerTask(record.id)
    Message.success('任务已触发执行')
    loadTasks()
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '触发失败')
  }
}

const handleViewLogs = (record: Task) => {
  router.push({
    name: 'ops-logs',
    query: {
      task_id: String(record.id),
      task_name: record.name || '',
      recent_days: '0',
    },
  })
}

const handleShowDetail = async (record: Task) => {
  detailVisible.value = true
  try {
    const data = await getTaskDetail(record.id)
    detailData.value = data
  } catch {
    detailData.value = record
  }
}

// 删除
const handleDelete = async (id: number) => {
  try {
    await deleteTask(id)
    Message.success('删除成功')
    loadTasks()
  } catch (error) {
    Message.error('删除失败')
  }
}

// 提交
const handleSubmit = async () => {
  try {
    if (!formData.name || !formData.cron_expression || !formData.server_ids?.length) {
      Message.warning('请填写任务名称、Cron表达式并选择目标服务器')
      return
    }
    if (formData.task_type === 'salt' && !selectedEnvironment.value) {
      Message.warning('SaltStack 任务请先选择环境')
      return
    }

    const payload: Partial<Task> = {
      name: formData.name,
      description: formData.description,
      script_id: formData.script_id,
      server_ids: formData.server_ids,
      cron_expression: formData.cron_expression,
      task_type: formData.task_type,
      command: formData.command,
      enabled: formData.enabled,
    }

    if (isEdit.value && editingId.value) {
      await updateTask(editingId.value, payload)
      Message.success('更新成功')
    } else {
      await createTask(payload)
      Message.success('创建成功')
    }
    modalVisible.value = false
    loadTasks()
  } catch (error) {
    Message.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

// 取消
const handleCancel = () => {
  modalVisible.value = false
  resetForm()
}

// 重置表单
const resetForm = () => {
  formData.name = ''
  formData.task_type = 'salt'
  formData.script_id = undefined
  formData.cron_expression = ''
  formData.server_ids = []
  formData.command = ''
  formData.enabled = true
  formData.description = ''
  selectedEnvironment.value = ''
}

onMounted(() => {
  loadServerOptions()
  loadScriptOptions()
  loadTasks()
})
</script>

<style scoped>
.task-list-container {
  padding: 20px;
}

.search-bar {
  margin-bottom: 16px;
}

.action-bar {
  margin-bottom: 16px;
}

.task-list-container :deep(.arco-table-cell) {
  vertical-align: middle;
}

.task-command-pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: Consolas, Monaco, 'Courier New', monospace;
  font-size: 12px;
  color: #334155;
}

</style>
