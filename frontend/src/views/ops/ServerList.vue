<template>
  <div class="server-list-container">
    <a-card :bordered="false">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <a-space>
          <a-input
            v-model="searchParams.name"
            placeholder="搜索服务器名称"
            allow-clear
            style="width: 200px"
            @press-enter="handleSearch"
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
          
          <a-select
            v-model="searchParams.environment"
            placeholder="环境"
            allow-clear
            style="width: 150px"
          >
            <a-option value="production">生产环境</a-option>
            <a-option value="staging">预发布环境</a-option>
            <a-option value="testing">测试环境</a-option>
          </a-select>
          
          <a-select
            v-model="searchParams.status"
            placeholder="状态"
            allow-clear
            style="width: 120px"
          >
            <a-option value="online">在线</a-option>
            <a-option value="offline">离线</a-option>
            <a-option value="unknown">未知</a-option>
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
          添加服务器
        </a-button>
      </div>

      <!-- 表格 -->
      <a-table
        :columns="columns"
        :data="serverList"
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
        
        <template #environment="{ record }">
          <a-tag :color="getEnvColor(record.environment)">
            {{ getEnvText(record.environment) }}
          </a-tag>
        </template>
        
        <template #auth_type="{ record }">
          <a-tag size="small">
            {{ record.auth_type === 'password' ? '密码' : '密钥' }}
          </a-tag>
        </template>
        
        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleTest(record)">
              测试连接
            </a-button>
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-popconfirm
              content="确定要删除该服务器吗？"
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
      width="700px"
      @ok="handleSubmit"
      @cancel="handleCancel"
    >
      <a-form :model="formData" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="服务器名称" required>
              <a-input v-model="formData.name" placeholder="例如：生产服务器-01" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="IP地址/域名" required>
              <a-input v-model="formData.hostname" placeholder="例如：192.168.1.100" />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="SSH端口">
              <a-input-number v-model="formData.port" :min="1" :max="65535" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="登录用户名">
              <a-input v-model="formData.username" placeholder="root" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="认证方式">
              <a-radio-group v-model="formData.auth_type">
                <a-radio value="password">密码</a-radio>
                <a-radio value="key">密钥</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-form-item v-if="formData.auth_type === 'password'" label="密码">
          <a-input-password v-model="formData.password" placeholder="SSH登录密码" />
        </a-form-item>
        
        <a-form-item v-else label="私钥内容">
          <a-textarea
            v-model="formData.private_key"
            :auto-size="{ minRows: 3, maxRows: 6 }"
            placeholder="SSH私钥内容"
          />
        </a-form-item>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="环境">
              <a-select v-model="formData.environment">
                <a-option value="production">生产环境</a-option>
                <a-option value="staging">预发布环境</a-option>
                <a-option value="testing">测试环境</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="Salt Minion ID">
              <a-input v-model="formData.salt_minion_id" placeholder="可选" />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-form-item label="描述">
          <a-textarea
            v-model="formData.description"
            :auto-size="{ minRows: 2, maxRows: 4 }"
            placeholder="服务器描述信息"
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
} from '@arco-design/web-vue/es/icon'
import {
  getServerList,
  createServer,
  updateServer,
  deleteServer,
  testServerConnection,
  type Server,
} from '@/api/ops/server'

// 搜索参数
const searchParams = reactive({
  name: '',
  environment: '',
  status: '',
})

// 表格数据
const serverList = ref<Server[]>([])
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
  { title: '服务器名称', dataIndex: 'name', width: 180 },
  { title: 'IP地址', dataIndex: 'hostname', width: 150 },
  { title: '端口', dataIndex: 'port', width: 80 },
  { title: '用户名', dataIndex: 'username', width: 100 },
  { title: '认证方式', slotName: 'auth_type', width: 100 },
  { title: '环境', slotName: 'environment', width: 120 },
  { title: '状态', slotName: 'status', width: 100 },
  { title: '描述', dataIndex: 'description', ellipsis: true, tooltip: true },
  { title: '创建时间', dataIndex: 'created_at', width: 180 },
  { title: '操作', slotName: 'actions', width: 200, fixed: 'right' },
]

// 模态框
const modalVisible = ref(false)
const modalTitle = ref('添加服务器')
const isEdit = ref(false)
const editingId = ref<number | null>(null)

const formData = reactive<Partial<Server>>({
  name: '',
  hostname: '',
  port: 22,
  username: 'root',
  auth_type: 'password',
  password: '',
  private_key: '',
  environment: 'production',
  salt_minion_id: '',
  description: '',
})

// 加载服务器列表
const loadServers = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      page_size: pagination.pageSize,
      ...searchParams,
    }
    const res = await getServerList(params)
    // 响应拦截器已经返回 response.data，所以 res 就是 {code, message, data, total}
    serverList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    console.error('加载服务器列表失败:', error)
    // 只有在真正的错误时才显示提示
    if (error.response && error.response.status !== 401) {
      Message.error('加载服务器列表失败: ' + (error.response?.data?.detail || error.message))
    }
    serverList.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadServers()
}

// 重置
const handleReset = () => {
  searchParams.name = ''
  searchParams.environment = ''
  searchParams.status = ''
  pagination.current = 1
  loadServers()
}

// 分页
const handlePageChange = (page: number) => {
  pagination.current = page
  loadServers()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize
  pagination.current = 1
  loadServers()
}

// 添加
const handleAdd = () => {
  isEdit.value = false
  modalTitle.value = '添加服务器'
  resetForm()
  modalVisible.value = true
}

// 编辑
const handleEdit = (record: Server) => {
  isEdit.value = true
  editingId.value = record.id
  modalTitle.value = '编辑服务器'
  Object.assign(formData, record)
  modalVisible.value = true
}

// 删除
const handleDelete = async (id: number) => {
  try {
    await deleteServer(id)
    Message.success('删除成功')
    loadServers()
  } catch (error) {
    Message.error('删除失败')
  }
}

// 测试连接
const handleTest = async (record: Server) => {
  try {
    const res = await testServerConnection({
      server_id: record.id,
      test_type: 'ssh',
    })
    if (res.code === 200) {
      Message.success('连接测试成功')
      loadServers()
    } else {
      Message.error(res.message || '连接测试失败')
    }
  } catch (error) {
    Message.error('连接测试失败')
  }
}

// 提交
const handleSubmit = async () => {
  try {
    if (isEdit.value && editingId.value) {
      await updateServer(editingId.value, formData)
      Message.success('更新成功')
    } else {
      await createServer(formData)
      Message.success('创建成功')
    }
    modalVisible.value = false
    loadServers()
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
  formData.hostname = ''
  formData.port = 22
  formData.username = 'root'
  formData.auth_type = 'password'
  formData.password = ''
  formData.private_key = ''
  formData.environment = 'production'
  formData.salt_minion_id = ''
  formData.description = ''
}

// 状态颜色
const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    online: 'green',
    offline: 'red',
    unknown: 'gray',
  }
  return colors[status] || 'gray'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    online: '在线',
    offline: '离线',
    unknown: '未知',
  }
  return texts[status] || status
}

// 环境颜色
const getEnvColor = (env: string) => {
  const colors: Record<string, string> = {
    production: 'red',
    staging: 'orange',
    testing: 'blue',
  }
  return colors[env] || 'gray'
}

const getEnvText = (env: string) => {
  const texts: Record<string, string> = {
    production: '生产',
    staging: '预发布',
    testing: '测试',
  }
  return texts[env] || env
}

onMounted(() => {
  loadServers()
})
</script>

<style scoped>
.server-list-container {
  padding: 20px;
}

.search-bar {
  margin-bottom: 16px;
}

.action-bar {
  margin-bottom: 16px;
}
</style>
