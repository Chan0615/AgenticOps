<template>
  <div class="task-page ant-illustration-page">
    <Card :bordered="false">
      <Space wrap style="margin-bottom: 16px">
        <Input v-model:value="searchParams.name" placeholder="搜索任务名称" allow-clear style="width: 220px" @pressEnter="handleSearch" />
        <Select v-model:value="searchParams.enabled" allow-clear placeholder="状态" style="width: 140px">
          <SelectOption :value="true">启用</SelectOption>
          <SelectOption :value="false">禁用</SelectOption>
        </Select>
        <Select v-model:value="searchParams.project_id" allow-clear placeholder="项目" style="width: 180px" @change="handleSearchProjectChange">
          <SelectOption v-for="item in projectOptions" :key="item.id" :value="item.id">{{ item.name }}</SelectOption>
        </Select>
        <Select v-model:value="searchParams.group_id" allow-clear placeholder="分组" style="width: 180px">
          <SelectOption v-for="item in searchGroupOptions" :key="item.id" :value="item.id">{{ item.name }}</SelectOption>
        </Select>
        <Button type="primary" @click="handleSearch">搜索</Button>
        <Button @click="handleReset">重置</Button>
      </Space>

      <div style="margin-bottom: 16px">
        <Button type="primary" @click="openModal()">创建任务</Button>
      </div>

      <div class="task-toolbar">
        <Space wrap>
          <Button :loading="checkingScheduler" @click="loadSchedulerHealth">Worker/Beat 健康检查</Button>
          <Button type="primary" ghost :loading="syncingScheduler" @click="handleSyncSchedule">立即同步任务</Button>
          <Space size="small">
            <span class="task-tip-inline">自动刷新（10分钟/次）</span>
            <Switch v-model:checked="autoRefreshHealth" size="small" />
          </Space>
          <Tag :color="schedulerHealth?.ok ? 'green' : 'red'">
            Worker: {{ schedulerHealth?.ok ? '正常' : '异常' }}
          </Tag>
          <Tag :color="schedulerHealth?.beat_healthy ? 'green' : 'orange'">
            Scheduler队列: {{ schedulerHealth?.beat_healthy ? '正常' : '未消费' }}
          </Tag>
          <span v-if="schedulerHealth?.missing_queues?.length" class="task-tip-inline">
            缺失队列: {{ schedulerHealth.missing_queues.join(', ') }}
          </span>
          <span v-if="healthCheckedAt" class="task-tip-inline">检查时间: {{ healthCheckedAt }}</span>
        </Space>
      </div>

      <Table :columns="columns" :data-source="taskList" :loading="loading" :pagination="pagination" row-key="id" @change="handleTableChange">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'group_info'">{{ record.project_name || '-' }} / {{ record.group_name || '-' }}</template>
          <template v-else-if="column.key === 'script_info'">
            <span v-if="record.script_id">{{ scriptNameMap[record.script_id] || `脚本#${record.script_id}` }}</span>
            <span v-else-if="record.command">内联命令</span>
            <span v-else>-</span>
          </template>
          <template v-else-if="column.key === 'enabled'">
            <Tag :color="record.enabled ? 'green' : 'red'">{{ record.enabled ? '已启用' : '已禁用' }}</Tag>
          </template>
          <template v-else-if="column.key === 'run_status'">
            <Tag :color="getRunStatusColor(record)">{{ getRunStatusText(record) }}</Tag>
          </template>
          <template v-else-if="column.key === 'last_run_at'">{{ formatDateTime(record.last_run_at) }}</template>
          <template v-else-if="column.key === 'next_run_at'">{{ formatDateTime(record.next_run_at) }}</template>
          <template v-else-if="column.key === 'created_at'">{{ formatDateTime(record.created_at) }}</template>
          <template v-else-if="column.key === 'targets'">
            <Space wrap>
              <Tag v-for="target in getTaskTargets(record).slice(0, 2)" :key="`${record.id}-${target.id}`" color="blue">
                {{ target.envText }} / {{ target.name }}
              </Tag>
              <Tag v-if="getTaskTargets(record).length > 2">+{{ getTaskTargets(record).length - 2 }}</Tag>
            </Space>
          </template>
          <template v-else-if="column.key === 'actions'">
            <Space>
              <Button type="link" @click="handleShowDetail(record)">详情</Button>
              <Button type="link" @click="handleTrigger(record)">测试</Button>
              <Button type="link" @click="handleViewLogs(record)">日志</Button>
              <Button type="link" @click="openModal(record)">编辑</Button>
              <Popconfirm title="确定要删除该任务吗？" @confirm="handleDelete(record.id)">
                <Button type="link" danger>删除</Button>
              </Popconfirm>
            </Space>
          </template>
        </template>
      </Table>
    </Card>

    <Modal v-model:open="modalOpen" :title="isEdit ? '编辑任务' : '创建任务'" width="900px" @ok="handleSubmit" @cancel="resetForm">
      <Form :model="formData" layout="vertical">
        <FormItem label="任务名称" required>
          <Input v-model:value="formData.name" placeholder="例如：每日日志清理" />
        </FormItem>

        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="所属项目" required>
              <Select v-model:value="formData.project_id" placeholder="请选择项目" @change="handleFormProjectChange">
                <SelectOption v-for="item in projectOptions" :key="item.id" :value="item.id">{{ item.name }}</SelectOption>
              </Select>
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="所属分组" required>
              <Select v-model:value="formData.group_id" :disabled="!formData.project_id" placeholder="请选择分组">
                <SelectOption v-for="item in formGroupOptions" :key="item.id" :value="item.id">{{ item.name }}</SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="Cron表达式" required>
              <Input v-model:value="formData.cron_expression" placeholder="例如：0 2 * * *" />
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="Salt环境" required>
              <Select v-model:value="selectedEnvironment" placeholder="选择环境后加载服务器" @change="formData.server_ids = []">
                <SelectOption v-for="item in environmentOptions" :key="item.value" :value="item.value">{{ item.label }}</SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <FormItem label="目标服务器" required>
          <Select v-model:value="formData.server_ids" mode="multiple" :loading="loadingServers" :disabled="!selectedEnvironment" placeholder="选择目标服务器">
            <SelectOption v-for="item in filteredServerOptions" :key="item.id" :value="item.id">{{ item.name }} ({{ item.hostname }})</SelectOption>
          </Select>
        </FormItem>

        <FormItem label="执行脚本（可选）">
          <Select v-model:value="formData.script_id" allow-clear placeholder="选择脚本（默认按 /root/ChAn/<文件名> 执行）" @change="handleScriptChange">
            <SelectOption v-for="item in filteredScriptOptions" :key="item.id" :value="item.id">{{ item.name }} ({{ item.source_file_name || scriptDisplayName(item) }})</SelectOption>
          </Select>
          <div class="task-tip">选中脚本且命令为空时，系统默认执行 `/root/ChAn/文件名`：Python 用 `python3`，Shell 用 `bash`。请先在脚本管理中分发到该目录。</div>
        </FormItem>

        <FormItem label="执行命令（可选）">
          <Input.TextArea v-model:value="formData.command" :rows="4" :placeholder="commandPlaceholder" />
          <div class="task-tip">可覆盖脚本默认执行方式；留空则走自动命令。</div>
        </FormItem>

        <FormItem label="描述">
          <Input v-model:value="formData.description" placeholder="任务描述" />
        </FormItem>

        <FormItem v-if="isEdit" label="任务状态">
          <RadioGroup v-model:value="formData.enabled">
            <Radio :value="true">启用</Radio>
            <Radio :value="false">禁用</Radio>
          </RadioGroup>
        </FormItem>
      </Form>
    </Modal>

    <Modal v-model:open="detailOpen" title="任务详情" width="860px" :footer="null">
      <Descriptions bordered :column="2">
        <DescriptionsItem label="任务名称">{{ detailData?.name || '-' }}</DescriptionsItem>
        <DescriptionsItem label="执行方式">SaltStack</DescriptionsItem>
        <DescriptionsItem label="项目/分组">{{ detailData?.project_name || '-' }} / {{ detailData?.group_name || '-' }}</DescriptionsItem>
        <DescriptionsItem label="脚本">{{ detailData?.script_id ? (scriptNameMap[detailData.script_id] || `脚本#${detailData.script_id}`) : '内联命令' }}</DescriptionsItem>
        <DescriptionsItem label="状态">
          <Tag :color="detailData?.enabled ? 'green' : 'red'">{{ detailData?.enabled ? '已启用' : '已禁用' }}</Tag>
        </DescriptionsItem>
        <DescriptionsItem label="Cron表达式">{{ detailData?.cron_expression || '-' }}</DescriptionsItem>
        <DescriptionsItem label="创建时间">{{ formatDateTime(detailData?.created_at) }}</DescriptionsItem>
        <DescriptionsItem label="更新时间">{{ formatDateTime(detailData?.updated_at) }}</DescriptionsItem>
        <DescriptionsItem label="上次执行">{{ formatDateTime(detailData?.last_run_at) }}</DescriptionsItem>
        <DescriptionsItem label="下次执行">{{ formatDateTime(detailData?.next_run_at) }}</DescriptionsItem>
        <DescriptionsItem label="描述" :span="2">{{ detailData?.description || '-' }}</DescriptionsItem>
        <DescriptionsItem label="执行命令" :span="2">
          <pre class="task-command">{{ detailData?.command || '-' }}</pre>
        </DescriptionsItem>
      </Descriptions>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Button,
  Card,
  Col,
  Descriptions,
  Form,
  Input,
  Modal,
  Popconfirm,
  Radio,
  Row,
  Select,
  Switch,
  Space,
  Table,
  Tag,
  message,
} from 'ant-design-vue'
import {
  createTask,
  deleteTask,
  getTaskDetail,
  getTaskList,
  getTaskSchedulerHealth,
  syncTaskSchedule,
  triggerTask,
  updateTask,
  type TaskSchedulerHealthData,
} from '@/api/ops/task'
import { getServerList, type Server } from '@/api/ops/server'
import { getScriptList } from '@/api/ops/script'
import { getGroupList, getProjectList, type OpsGroup, type OpsProject } from '@/api/ops/group'
import { formatDateTime } from '@/utils/datetime'

const FormItem = Form.Item
const SelectOption = Select.Option
const DescriptionsItem = Descriptions.Item
const RadioGroup = Radio.Group

const router = useRouter()

interface Task {
  id: number
  name: string
  project_id?: number
  group_id?: number
  project_name?: string
  group_name?: string
  description?: string
  script_id?: number
  server_ids: number[]
  cron_expression: string
  task_type: 'salt'
  command?: string
  enabled: boolean
  last_run_at?: string
  next_run_at?: string
  created_at: string
  updated_at: string
}

interface TaskServerOption {
  id: number
  name: string
  hostname: string
  environment: string
}

const searchParams = reactive({
  name: '',
  enabled: undefined as boolean | undefined,
  project_id: undefined as number | undefined,
  group_id: undefined as number | undefined,
})

const projectOptions = ref<OpsProject[]>([])
const groupOptions = ref<OpsGroup[]>([])
const searchGroupOptions = computed(() => {
  if (!searchParams.project_id) return groupOptions.value
  return groupOptions.value.filter((g) => g.project_id === searchParams.project_id)
})

const taskList = ref<Task[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
})

const columns = [
  { title: '任务', dataIndex: 'name', key: 'name', width: 160 },
  { title: '项目/分组', key: 'group_info', width: 220 },
  { title: '脚本', key: 'script_info', width: 160 },
  { title: '执行态', key: 'run_status', width: 100 },
  { title: '上次执行', key: 'last_run_at', width: 170 },
  { title: '下次执行', key: 'next_run_at', width: 170 },
  { title: '目标主机', key: 'targets', width: 260 },
  { title: 'Cron', dataIndex: 'cron_expression', key: 'cron_expression', width: 140 },
  { title: '状态', key: 'enabled', width: 100 },
  { title: '创建时间', key: 'created_at', width: 170 },
  { title: '操作', key: 'actions', width: 260, fixed: 'right' as const },
]

const modalOpen = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const detailOpen = ref(false)
const detailData = ref<Task | null>(null)

const formData = reactive<Partial<Task>>({
  name: '',
  project_id: undefined,
  group_id: undefined,
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
const scriptOptions = ref<Array<{ id: number; name: string; group_id?: number; script_type?: string; source_file_name?: string }>>([])
const checkingScheduler = ref(false)
const syncingScheduler = ref(false)
const schedulerHealth = ref<TaskSchedulerHealthData | null>(null)
const autoRefreshHealth = ref(true)
const healthCheckedAt = ref('')
let healthTimer: number | null = null
const formGroupOptions = computed(() => {
  if (!formData.project_id) return []
  return groupOptions.value.filter((g) => g.project_id === formData.project_id)
})
const filteredScriptOptions = computed(() => {
  if (!formData.group_id) return scriptOptions.value
  return scriptOptions.value.filter((s) => s.group_id === formData.group_id)
})

const selectedScript = computed(() => scriptOptions.value.find((s) => s.id === formData.script_id))

const commandPlaceholder = computed(() => {
  if (selectedScript.value?.script_type === 'python') {
    return "可留空自动执行：python3 /root/ChAn/<脚本文件名>；或输入自定义命令，例如：python3 /root/ChAn/main.py --env prod"
  }
  if (selectedScript.value?.script_type === 'shell') {
    return "可留空自动执行：bash /root/ChAn/<脚本文件名>；或输入自定义命令，例如：bash /root/ChAn/deploy.sh"
  }
  return '不选脚本时请输入要执行的命令...'
})

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
  if (!selectedEnvironment.value) return []
  return serverOptions.value.filter((s) => s.environment === selectedEnvironment.value)
})

const getTaskTargets = (task: Task) => {
  return (task.server_ids || []).map((id) => {
    const server = serverOptions.value.find((s) => s.id === id)
    if (!server) {
      return { id, name: `主机#${id}`, envText: '未知环境' }
    }
    return {
      id,
      name: server.name,
      envText: envTextMap[server.environment] || server.environment,
    }
  })
}

const getRunStatusText = (task: Task) => {
  if (!task.enabled) return '已停用'
  if (task.last_run_at) return '已执行'
  return '待执行'
}

const getRunStatusColor = (task: Task) => {
  if (!task.enabled) return 'default'
  if (task.last_run_at) return 'green'
  return 'orange'
}

const loadGroupMeta = async () => {
  try {
    const [projectRes, groupRes] = await Promise.all([
      getProjectList({ page: 1, page_size: 200 }),
      getGroupList({ page: 1, page_size: 200 }),
    ])
    projectOptions.value = projectRes.data || []
    groupOptions.value = groupRes.data || []
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载项目分组失败')
  }
}

const loadServerOptions = async () => {
  loadingServers.value = true
  try {
    const res = await getServerList({ page: 1, page_size: 200 })
    serverOptions.value = (res.data || []).map((s: Server) => ({
      id: s.id,
      name: s.name,
      hostname: s.hostname,
      environment: s.environment,
    }))
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载服务器列表失败')
    serverOptions.value = []
  } finally {
    loadingServers.value = false
  }
}

const loadScriptOptions = async () => {
  try {
    const res = await getScriptList({ page: 1, page_size: 200 })
    const items = res.data || []
    scriptOptions.value = items.map((s) => ({
      id: s.id,
      name: s.name,
      group_id: s.group_id,
      script_type: s.script_type,
      source_file_name: s.source_file_name,
    }))
    items.forEach((s) => {
      scriptNameMap[s.id] = s.name
    })
  } catch {
    scriptOptions.value = []
  }
}

const loadTasks = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (searchParams.name) params.name = searchParams.name
    if (typeof searchParams.enabled === 'boolean') params.enabled = searchParams.enabled
    if (searchParams.project_id) params.project_id = searchParams.project_id
    if (searchParams.group_id) params.group_id = searchParams.group_id

    const res = await getTaskList(params)
    taskList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载任务列表失败')
    taskList.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.current = 1
  loadTasks()
}

const handleReset = () => {
  searchParams.name = ''
  searchParams.enabled = undefined
  searchParams.project_id = undefined
  searchParams.group_id = undefined
  pagination.current = 1
  loadTasks()
}

const handleSearchProjectChange = () => {
  searchParams.group_id = undefined
}

const handleTableChange = (pageInfo: any) => {
  pagination.current = pageInfo.current
  pagination.pageSize = pageInfo.pageSize
  loadTasks()
}

const openModal = async (record?: Task) => {
  // 先打开弹窗，服务器列表后台刷新，避免点击后等待网络请求
  if (!serverOptions.value.length && !loadingServers.value) {
    loadServerOptions()
  }
  if (record) {
    isEdit.value = true
    editingId.value = record.id
    Object.assign(formData, record)
    if (!formData.project_id && formData.group_id) {
      const group = groupOptions.value.find((g) => g.id === formData.group_id)
      formData.project_id = group?.project_id
    }
    if (record.server_ids?.length) {
      const envSet = new Set(
        record.server_ids
          .map((id) => serverOptions.value.find((s) => s.id === id)?.environment)
          .filter((v): v is string => !!v),
      )
      selectedEnvironment.value = envSet.size === 1 ? Array.from(envSet)[0] : ''
    }
  } else {
    resetForm()
    isEdit.value = false
  }
  modalOpen.value = true

  // 弹窗打开后异步刷新一次服务器列表（不阻塞交互）
  if (!loadingServers.value) {
    loadServerOptions()
  }
}

const resetForm = () => {
  modalOpen.value = false
  isEdit.value = false
  editingId.value = null
  formData.name = ''
  formData.project_id = undefined
  formData.group_id = undefined
  formData.task_type = 'salt'
  formData.script_id = undefined
  formData.cron_expression = ''
  formData.server_ids = []
  formData.command = ''
  formData.enabled = true
  formData.description = ''
  selectedEnvironment.value = ''
}

const handleFormProjectChange = () => {
  formData.group_id = undefined
  formData.script_id = undefined
}

const scriptDisplayName = (item: { name: string; script_type?: string }) => {
  return `${item.name}${item.script_type === 'python' ? '.py' : '.sh'}`
}

const handleScriptChange = () => {
  // Keep command untouched to avoid overriding user input.
}

const handleSubmit = async () => {
  if (!formData.name || !formData.cron_expression || !formData.server_ids?.length) {
    message.warning('请填写任务名称、Cron表达式并选择目标服务器')
    return
  }
  if (!formData.script_id && !String(formData.command || '').trim()) {
    message.warning('请选择脚本，或填写执行命令')
    return
  }
  if (!formData.project_id || !formData.group_id) {
    message.warning('请选择所属项目和分组')
    return
  }
  if (!selectedEnvironment.value) {
    message.warning('请选择 Salt 环境')
    return
  }

  const payload: Partial<Task> = {
    name: formData.name,
    project_id: formData.project_id,
    group_id: formData.group_id,
    description: formData.description,
    script_id: formData.script_id,
    server_ids: formData.server_ids,
    cron_expression: formData.cron_expression,
    task_type: 'salt',
    command: formData.command,
    enabled: formData.enabled,
  }

  try {
    if (isEdit.value && editingId.value) {
      await updateTask(editingId.value, payload)
      message.success('任务更新成功')
    } else {
      await createTask(payload)
      message.success('任务创建成功')
    }
    resetForm()
    loadTasks()
  } catch (error: any) {
    message.error(error.response?.data?.detail || (isEdit.value ? '任务更新失败' : '任务创建失败'))
  }
}

const handleTrigger = async (record: Task) => {
  try {
    await triggerTask(record.id)
    message.success('任务已触发')
    loadTasks()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '触发失败')
  }
}

const loadSchedulerHealth = async () => {
  checkingScheduler.value = true
  try {
    const res = await getTaskSchedulerHealth()
    schedulerHealth.value = res.data
    healthCheckedAt.value = new Date().toLocaleString()
  } catch (error: any) {
    schedulerHealth.value = null
    message.error(error.response?.data?.detail || '健康检查失败')
  } finally {
    checkingScheduler.value = false
  }
}

const startHealthTimer = () => {
  if (healthTimer !== null) return
  healthTimer = window.setInterval(() => {
    if (!autoRefreshHealth.value || checkingScheduler.value || syncingScheduler.value) return
    loadSchedulerHealth()
  }, 600000)
}

const stopHealthTimer = () => {
  if (healthTimer !== null) {
    clearInterval(healthTimer)
    healthTimer = null
  }
}

const handleSyncSchedule = async () => {
  syncingScheduler.value = true
  try {
    await syncTaskSchedule()
    message.success('已触发一次调度扫描')
    await loadSchedulerHealth()
    await loadTasks()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '同步任务失败')
  } finally {
    syncingScheduler.value = false
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
  detailOpen.value = true
  try {
    detailData.value = await getTaskDetail(record.id)
  } catch {
    detailData.value = record
  }
}

const handleDelete = async (id: number) => {
  try {
    await deleteTask(id)
    message.success('删除成功')
    loadTasks()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '删除失败')
  }
}

onMounted(async () => {
  await loadGroupMeta()
  await loadServerOptions()
  await loadScriptOptions()
  await loadSchedulerHealth()
  startHealthTimer()
  await loadTasks()
})

onUnmounted(() => {
  stopHealthTimer()
})
</script>

<style scoped>
.task-toolbar {
  margin-bottom: 16px;
}

.task-command {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: Consolas, Monaco, 'Courier New', monospace;
  font-size: 12px;
  color: #334155;
}

.task-tip-inline {
  color: #64748b;
  font-size: 12px;
}

.task-tip {
  margin-top: 6px;
  font-size: 12px;
  color: #64748b;
}
</style>
