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
        :scroll="{ x: 1280 }"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #enabled="{ record }">
          <a-space>
            <a-switch
              v-model="record.enabled"
              checked-text="启用"
              unchecked-text="禁用"
              @change="handleToggle(record)"
            />
            <a-tag :color="record.enabled ? 'green' : 'red'">
              {{ record.enabled ? '已启用' : '已禁用' }}
            </a-tag>
          </a-space>
        </template>
        
        <template #task_type="{ record }">
          <a-tag :color="record.task_type === 'salt' ? 'purple' : 'orange'">
            {{ record.task_type === 'salt' ? 'SaltStack' : 'JumpServer' }}
          </a-tag>
        </template>
        
        <template #actions="{ record }">
          <a-space>
            <a-tag color="blue" @click="handleTrigger(record)" :hoverable="true">
              执行
            </a-tag>
            <a-tag @click="handleEdit(record)" :hoverable="true">
              编辑
            </a-tag>
            <a-popconfirm
              content="确定要删除该任务吗？"
              @ok="handleDelete(record.id)"
            >
              <a-tag color="red" size="small" :hoverable="true">
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
              <a-select v-model="formData.task_type">
                <a-option value="salt">SaltStack</a-option>
                <a-option value="jumpserver">JumpServer</a-option>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { Message } from '@arco-design/web-vue'
import {
  IconSearch,
  IconRefresh,
  IconPlus,
  IconQuestionCircle,
} from '@arco-design/web-vue/es/icon'
import { getTaskList, createTask, updateTask, toggleTask, triggerTask, deleteTask } from '@/api/ops/task'
import { getServerList, type Server } from '@/api/ops/server'

interface Task {
  id: number
  name: string
  description?: string
  script_id?: number
  server_ids: number[]
  cron_expression: string
  task_type: string
  command?: string
  enabled: boolean
  celery_task_id?: string
  last_run_at?: string
  next_run_at?: string
  created_by?: string
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
  { title: '任务名称', dataIndex: 'name', width: 180 },
  { title: '执行方式', slotName: 'task_type', width: 120 },
  { title: 'Cron表达式', dataIndex: 'cron_expression', width: 150 },
  { title: '状态', slotName: 'enabled', width: 180 },
  { title: '上次执行', dataIndex: 'last_run_at', width: 180 },
  { title: '下次执行', dataIndex: 'next_run_at', width: 180 },
  { title: '创建时间', dataIndex: 'created_at', width: 180 },
  { title: '操作', slotName: 'actions', width: 200, fixed: 'right' },
]

// 模态框
const modalVisible = ref(false)
const modalTitle = ref('创建任务')
const isEdit = ref(false)
const editingId = ref<number | null>(null)

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

const environmentOptions = [
  { label: '富春云', value: 'fuchunyun' },
  { label: '阿里云', value: 'aliyun' },
  { label: '滨江', value: 'binjiang' },
  { label: '阿里云压测', value: 'aliyunyc' },
]

const filteredServerOptions = computed(() => {
  if (formData.task_type !== 'salt') return serverOptions.value
  if (!selectedEnvironment.value) return []
  return serverOptions.value.filter(s => s.environment === selectedEnvironment.value)
})

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
  } catch (error) {
    Message.error('触发失败')
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
  formData.cron_expression = ''
  formData.server_ids = []
  formData.command = ''
  formData.enabled = true
  formData.description = ''
  selectedEnvironment.value = ''
}

onMounted(() => {
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
</style>
