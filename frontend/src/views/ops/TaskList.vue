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
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #enabled="{ record }">
          <a-switch
            v-model="record.enabled"
            @change="handleToggle(record)"
          />
        </template>
        
        <template #task_type="{ record }">
          <a-tag :color="record.task_type === 'salt' ? 'purple' : 'orange'">
            {{ record.task_type === 'salt' ? 'SaltStack' : 'SSH' }}
          </a-tag>
        </template>
        
        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleTrigger(record)">
              执行
            </a-button>
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-popconfirm
              content="确定要删除该任务吗？"
              @ok="handleDelete(record.id)"
            >
              <a-button type="text" size="small" status="danger">
                删除
              </a-button>
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
                <a-option value="ssh">SSH</a-option>
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
        
        <a-form-item label="目标服务器" required>
          <a-select
            v-model="formData.server_ids"
            multiple
            placeholder="选择目标服务器"
          >
            <!-- TODO: 从服务器列表加载 -->
            <a-option :value="1">服务器-01</a-option>
            <a-option :value="2">服务器-02</a-option>
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
import { ref, reactive, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import {
  IconSearch,
  IconRefresh,
  IconPlus,
  IconQuestionCircle,
} from '@arco-design/web-vue/es/icon'
import { getTaskList, toggleTask, triggerTask, deleteTask } from '@/api/ops/task'

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
  { title: 'ID', dataIndex: 'id', width: 80 },
  { title: '任务名称', dataIndex: 'name', width: 180 },
  { title: '执行方式', slotName: 'task_type', width: 120 },
  { title: 'Cron表达式', dataIndex: 'cron_expression', width: 150 },
  { title: '状态', slotName: 'enabled', width: 100 },
  { title: '上次执行', dataIndex: 'last_run_at', width: 180 },
  { title: '下次执行', dataIndex: 'next_run_at', width: 180 },
  { title: '创建时间', dataIndex: 'created_at', width: 180 },
  { title: '操作', slotName: 'actions', width: 180, fixed: 'right' },
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

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const res = await getTaskList({
      page: pagination.current,
      page_size: pagination.pageSize,
      ...searchParams,
    })
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
}

// 编辑
const handleEdit = (record: Task) => {
  isEdit.value = true
  editingId.value = record.id
  modalTitle.value = '编辑任务'
  Object.assign(formData, record)
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
    // TODO: 调用 API
    Message.success(isEdit.value ? '更新成功（待实现API）' : '创建成功（待实现API）')
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
</style>
