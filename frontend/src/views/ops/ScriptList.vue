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
        :scroll="{ x: 1200 }"
        table-layout-fixed
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
            <a-tag color="blue" @click="handleView(record)" :hoverable="true">
              查看
            </a-tag>
            <a-tag color="arcoblue" @click="openDistribute(record)" :hoverable="true">
              分发
            </a-tag>
            <a-tag @click="handleEdit(record)" :hoverable="true">
              编辑
            </a-tag>
            <a-popconfirm
              content="确定要删除该脚本吗？"
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
        
        <a-form-item label="上传脚本文件" required>
          <input
            ref="fileInputRef"
            type="file"
            accept=".sh,.py,.bash,.txt"
            style="display: none"
            @change="onFileInputChange"
          />
          <a-space>
            <a-button type="outline" @click="triggerFileSelect">选择脚本文件</a-button>
          </a-space>
          <div v-if="selectedFileName" style="margin-top: 8px;">
            <a-tag color="arcoblue" closable @close="handleFileRemove">
              已选择: {{ selectedFileName }}
            </a-tag>
          </div>
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

    <a-modal
      v-model:visible="distributeVisible"
      title="分发脚本"
      width="720px"
      @ok="handleDistributeSubmit"
      @cancel="handleDistributeCancel"
    >
      <a-form :model="distributeForm" layout="vertical">
        <a-form-item label="脚本">
          <a-input :model-value="distributingScript?.name || ''" disabled />
        </a-form-item>

        <a-form-item label="目标服务器" required>
          <a-select
            v-model="distributeForm.server_ids"
            multiple
            allow-search
            placeholder="请选择服务器"
          >
            <a-option v-for="s in serverOptions" :key="s.id" :value="s.id">
              {{ s.name }} ({{ s.hostname }})
            </a-option>
          </a-select>
        </a-form-item>

        <a-form-item label="目标目录" required>
          <a-input v-model="distributeForm.target_directory" placeholder="例如：/opt/scripts" />
        </a-form-item>

        <a-form-item label="目标文件名（可选）">
          <a-input v-model="distributeForm.file_name" placeholder="例如：deploy.sh" />
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
      <a-spin :loading="viewLoading" style="width: 100%">
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="脚本名称">
          {{ viewData.name }}
        </a-descriptions-item>
        <a-descriptions-item label="脚本类型">
          <a-tag :color="viewData.script_type === 'shell' ? 'green' : 'blue'">
            {{ (viewData.script_type || '').toUpperCase() }}
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
      <div class="script-content" v-html="highlightedContent"></div>
      </a-spin>
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
} from '@arco-design/web-vue/es/icon'
import { getScriptList, getScriptDetail, deleteScript, updateScript, uploadScript, replaceScriptFile, distributeScript } from '@/api/ops/script'
import { getServerList, type Server } from '@/api/ops/server'
import hljs from 'highlight.js/lib/core'
import python from 'highlight.js/lib/languages/python'
import bash from 'highlight.js/lib/languages/bash'
import 'highlight.js/styles/github-dark.css'

hljs.registerLanguage('python', python)
hljs.registerLanguage('bash', bash)

interface Script {
  id: number
  name: string
  description?: string
  content?: string
  file_path?: string
  source_file_name?: string
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
  { title: '脚本', dataIndex: 'name', width: 200 },
  { title: '类型', slotName: 'script_type', width: 100 },
  { title: '超时', slotName: 'timeout', width: 90 },
  { title: '描述', dataIndex: 'description', width: 260, ellipsis: true, tooltip: true },
  { title: '创建人', dataIndex: 'created_by', width: 90 },
  { title: '创建', dataIndex: 'created_at', width: 170 },
  { title: '操作', slotName: 'actions', width: 220 },
]

// 模态框
const modalVisible = ref(false)
const modalTitle = ref('创建脚本')
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)
const selectedUploadFile = ref<File | null>(null)
const selectedFileName = ref('')

const distributeVisible = ref(false)
const distributingScript = ref<Script | null>(null)
const serverOptions = ref<Server[]>([])
const distributeForm = reactive({
  server_ids: [] as number[],
  target_directory: '/opt/scripts',
  file_name: '',
})

const formData = reactive<Partial<Script>>({
  name: '',
  script_type: 'shell',
  timeout: 300,
  description: '',
})

// 查看
const viewVisible = ref(false)
const viewData = ref<Script>({} as Script)
const viewLoading = ref(false)
const highlightedContent = computed(() => {
  const raw = viewData.value?.content || '暂无脚本内容'
  if (!viewData.value?.content) {
    return `<pre><code>${raw}</code></pre>`
  }
  const lang = viewData.value.script_type === 'python' ? 'python' : 'bash'
  const html = hljs.highlight(raw, { language: lang }).value
  return `<pre><code class="hljs language-${lang}">${html}</code></pre>`
})

// 加载脚本列表
const loadScripts = async () => {
  loading.value = true
  try {
    const res = await getScriptList({
      page: pagination.current,
      page_size: pagination.pageSize,
      ...searchParams,
    })
    scriptList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    console.error('加载脚本列表失败:', error)
    if (error.response && error.response.status !== 401) {
      Message.error('加载脚本列表失败: ' + (error.response?.data?.detail || error.message))
    }
    scriptList.value = []
    pagination.total = 0
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
  selectedUploadFile.value = null
  selectedFileName.value = ''
  modalVisible.value = true
}

// 查看
const handleView = async (record: Script) => {
  viewVisible.value = true
  viewLoading.value = true
  try {
    const detail = await getScriptDetail(record.id)
    viewData.value = detail
  } catch (error: any) {
    viewData.value = record
    Message.error(error.response?.data?.detail || '加载脚本详情失败')
  } finally {
    viewLoading.value = false
  }
}

// 删除
const handleDelete = async (id: number) => {
  try {
    await deleteScript(id)
    Message.success('删除成功')
    loadScripts()
  } catch (error) {
    Message.error('删除失败')
  }
}

// 提交
const handleSubmit = async () => {
  try {
    if (!selectedUploadFile.value) {
      Message.warning('请上传脚本文件')
      return
    }

    const fd = new FormData()
    fd.append('file', selectedUploadFile.value)

    if (isEdit.value && editingId.value) {
      await replaceScriptFile(editingId.value, fd)
      await updateScript(editingId.value, {
        name: formData.name,
        description: formData.description,
        script_type: formData.script_type,
        timeout: formData.timeout,
      })
      Message.success('更新成功')
    } else {
      if (formData.name) fd.append('name', formData.name)
      if (formData.description) fd.append('description', formData.description)
      if (formData.script_type) fd.append('script_type', formData.script_type)
      if (formData.timeout) fd.append('timeout', String(formData.timeout))
      await uploadScript(fd)
      Message.success('创建成功')
    }
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
  formData.script_type = 'shell'
  formData.timeout = 300
  formData.description = ''
  selectedUploadFile.value = null
  selectedFileName.value = ''
}

const triggerFileSelect = () => {
  fileInputRef.value?.click()
}

const onFileInputChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] || null
  selectedUploadFile.value = file
  selectedFileName.value = file?.name || ''
}

const handleFileRemove = () => {
  selectedUploadFile.value = null
  selectedFileName.value = ''
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}


const openDistribute = async (record: Script) => {
  distributingScript.value = record
  distributeForm.server_ids = []
  distributeForm.target_directory = '/opt/scripts'
  distributeForm.file_name = record.source_file_name || `${record.name}${record.script_type === 'python' ? '.py' : '.sh'}`
  distributeVisible.value = true
  await loadDistributeServers()
}

const loadDistributeServers = async () => {
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

    serverOptions.value = allServers
  } catch (error) {
    Message.error('加载服务器列表失败')
    serverOptions.value = []
  }
}

const handleDistributeSubmit = async () => {
  if (!distributingScript.value) return
  if (!distributeForm.server_ids.length) {
    Message.warning('请选择目标服务器')
    return
  }
  if (!distributeForm.target_directory) {
    Message.warning('请输入目标目录')
    return
  }

  try {
    const res = await distributeScript(distributingScript.value.id, {
      server_ids: distributeForm.server_ids,
      target_directory: distributeForm.target_directory,
      file_name: distributeForm.file_name || undefined,
    })
    const failedResults = (res.data?.results || []).filter((item: any) => !item.success)
    if (res.code === 200 && failedResults.length === 0) {
      Message.success(res.message || '脚本分发完成')
    } else {
      const firstError = failedResults[0]?.message
      Message.warning(firstError ? `${res.message}，失败原因：${firstError}` : (res.message || '脚本分发部分失败'))
    }
    distributeVisible.value = false
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '脚本分发失败')
  }
}

const handleDistributeCancel = () => {
  distributeVisible.value = false
  distributingScript.value = null
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

.script-list-container :deep(.arco-table-th),
.script-list-container :deep(.arco-table-td) {
  vertical-align: middle;
  white-space: nowrap;
}

.script-content {
  background: #0d1117;
  border-radius: 8px;
  overflow-x: auto;
  max-height: 400px;
}

.script-content :deep(pre) {
  margin: 0;
  padding: 16px;
  font-size: 13px;
  line-height: 1.6;
}
</style>
