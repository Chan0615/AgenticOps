<template>
  <div class="script-list-container">
    <a-card :bordered="false">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <a-space>
          <a-input
            v-model="searchParams.name"
            placeholder="搜索脚本名称"
            allow-clear
            style="width: 200px"
            @press-enter="handleSearch"
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
          
          <a-select
            v-model="searchParams.script_type"
            placeholder="脚本类型"
            allow-clear
            style="width: 150px"
          >
            <a-option value="shell">Shell</a-option>
            <a-option value="python">Python</a-option>
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
          创建脚本
        </a-button>
      </div>

      <!-- 表格 -->
      <a-table
        :columns="columns"
        :data="scriptList"
        :loading="loading"
        :pagination="pagination"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #script_type="{ record }">
          <a-tag :color="record.script_type === 'shell' ? 'green' : 'blue'">
            {{ record.script_type.toUpperCase() }}
          </a-tag>
        </template>
        
        <template #timeout="{ record }">
          {{ record.timeout }}秒
        </template>
        
        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleView(record)">
              查看
            </a-button>
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-popconfirm
              content="确定要删除该脚本吗？"
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
      width="900px"
      @ok="handleSubmit"
      @cancel="handleCancel"
    >
      <a-form :model="formData" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="脚本名称" required>
              <a-input v-model="formData.name" placeholder="例如：日志清理脚本" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="脚本类型" required>
              <a-select v-model="formData.script_type">
                <a-option value="shell">Shell</a-option>
                <a-option value="python">Python</a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-form-item label="脚本内容" required>
          <a-textarea
            v-model="formData.content"
            :auto-size="{ minRows: 10, maxRows: 20 }"
            placeholder="输入脚本内容..."
            style="font-family: monospace"
          />
        </a-form-item>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="超时时间（秒）">
              <a-input-number
                v-model="formData.timeout"
                :min="1"
                :max="3600"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-form-item label="描述">
          <a-textarea
            v-model="formData.description"
            :auto-size="{ minRows: 2, maxRows: 4 }"
            placeholder="脚本描述信息"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看对话框 -->
    <a-modal
      v-model:visible="viewVisible"
      title="查看脚本"
      width="900px"
      :footer="false"
    >
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="脚本名称">
          {{ viewData.name }}
        </a-descriptions-item>
        <a-descriptions-item label="脚本类型">
          <a-tag :color="viewData.script_type === 'shell' ? 'green' : 'blue'">
            {{ viewData.script_type.toUpperCase() }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="超时时间">
          {{ viewData.timeout }}秒
        </a-descriptions-item>
        <a-descriptions-item label="创建人">
          {{ viewData.created_by || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="创建时间" :span="2">
          {{ viewData.created_at }}
        </a-descriptions-item>
        <a-descriptions-item label="描述" :span="2">
          {{ viewData.description || '-' }}
        </a-descriptions-item>
      </a-descriptions>
      
      <a-divider>脚本内容</a-divider>
      <pre class="script-content">{{ viewData.content }}</pre>
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
} from '@arco-design/web-vue/es/icon'

interface Script {
  id: number
  name: string
  description?: string
  content: string
  script_type: string
  parameters?: any[]
  timeout: number
  created_by?: string
  created_at: string
  updated_at: string
}

// 搜索参数
const searchParams = reactive({
  name: '',
  script_type: '',
})

// 表格数据
const scriptList = ref<Script[]>([])
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
  { title: '脚本名称', dataIndex: 'name', width: 200 },
  { title: '类型', slotName: 'script_type', width: 100 },
  { title: '超时时间', slotName: 'timeout', width: 100 },
  { title: '描述', dataIndex: 'description', ellipsis: true, tooltip: true },
  { title: '创建人', dataIndex: 'created_by', width: 100 },
  { title: '创建时间', dataIndex: 'created_at', width: 180 },
  { title: '操作', slotName: 'actions', width: 180, fixed: 'right' },
]

// 模态框
const modalVisible = ref(false)
const modalTitle = ref('创建脚本')
const isEdit = ref(false)
const editingId = ref<number | null>(null)

const formData = reactive<Partial<Script>>({
  name: '',
  content: '',
  script_type: 'shell',
  timeout: 300,
  description: '',
})

// 查看
const viewVisible = ref(false)
const viewData = ref<Script>({} as Script)

// 加载脚本列表
const loadScripts = async () => {
  loading.value = true
  try {
    // TODO: 调用 API
    // const res = await getScriptList({
    //   page: pagination.current,
    //   page_size: pagination.pageSize,
    //   ...searchParams,
    // })
    // scriptList.value = res.data
    // pagination.total = res.total
    
    // 临时数据
    scriptList.value = []
    pagination.total = 0
  } catch (error) {
    Message.error('加载脚本列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadScripts()
}

// 重置
const handleReset = () => {
  searchParams.name = ''
  searchParams.script_type = ''
  pagination.current = 1
  loadScripts()
}

// 分页
const handlePageChange = (page: number) => {
  pagination.current = page
  loadScripts()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize
  pagination.current = 1
  loadScripts()
}

// 添加
const handleAdd = () => {
  isEdit.value = false
  modalTitle.value = '创建脚本'
  resetForm()
  modalVisible.value = true
}

// 编辑
const handleEdit = (record: Script) => {
  isEdit.value = true
  editingId.value = record.id
  modalTitle.value = '编辑脚本'
  Object.assign(formData, record)
  modalVisible.value = true
}

// 查看
const handleView = (record: Script) => {
  viewData.value = record
  viewVisible.value = true
}

// 删除
const handleDelete = async (id: number) => {
  try {
    // TODO: 调用 API
    // await deleteScript(id)
    Message.success('删除成功')
    loadScripts()
  } catch (error) {
    Message.error('删除失败')
  }
}

// 提交
const handleSubmit = async () => {
  try {
    // TODO: 调用 API
    // if (isEdit.value && editingId.value) {
    //   await updateScript(editingId.value, formData)
    //   Message.success('更新成功')
    // } else {
    //   await createScript(formData)
    //   Message.success('创建成功')
    // }
    Message.success(isEdit.value ? '更新成功（待实现API）' : '创建成功（待实现API）')
    modalVisible.value = false
    loadScripts()
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
  formData.content = ''
  formData.script_type = 'shell'
  formData.timeout = 300
  formData.description = ''
}

onMounted(() => {
  loadScripts()
})
</script>

<style scoped>
.script-list-container {
  padding: 20px;
}

.search-bar {
  margin-bottom: 16px;
}

.action-bar {
  margin-bottom: 16px;
}

.script-content {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  max-height: 400px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
