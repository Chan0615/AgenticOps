<template>
  <div class="server-management">
    <a-card title="服务器管理" :bordered="false">
      <template #extra>
        <a-space>
          <a-button type="primary" @click="showAddServerModal">
            <template #icon><icon-plus /></template>
            添加服务器
          </a-button>
          <a-button @click="loadServers">
            <template #icon><icon-refresh /></template>
            刷新
          </a-button>
        </a-space>
      </template>

      <!-- 搜索栏 -->
      <a-form layout="inline" class="search-form">
        <a-form-item label="搜索">
          <a-input
            v-model="searchKeyword"
            placeholder="搜索服务器名称、IP、用户名..."
            allow-clear
            style="width: 300px"
            @press-enter="handleSearch"
          >
            <template #prefix><icon-search /></template>
          </a-input>
        </a-form-item>
        <a-form-item label="环境">
          <a-select
            v-model="selectedEnvironment"
            placeholder="全部环境"
            allow-clear
            style="width: 150px"
            @change="handleSearch"
          >
            <a-option v-for="env in environments" :key="env.value" :value="env.value">
              {{ env.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select
            v-model="statusFilter"
            placeholder="全部状态"
            allow-clear
            style="width: 120px"
            @change="handleSearch"
          >
            <a-option :value="true">在线</a-option>
            <a-option :value="false">离线</a-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">
            <template #icon><icon-search /></template>
            搜索
          </a-button>
        </a-form-item>
        <a-form-item>
          <a-button @click="resetSearch">
            <template #icon><icon-refresh /></template>
            重置
          </a-button>
        </a-form-item>
      </a-form>

      <!-- 服务器列表 -->
      <a-table
        :columns="columns"
        :data="serverList"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #status="{ record }">
          <a-tag :color="record.is_connected ? 'green' : 'red'">
            <template #icon>
              <icon-check-circle v-if="record.is_connected" />
              <icon-close-circle v-else />
            </template>
            {{ record.is_connected ? '在线' : '离线' }}
          </a-tag>
        </template>
        <template #environment="{ record }">
          <a-tag v-if="record.group" color="arcoblue">
            {{ getEnvironmentLabel(record.group.environment) }}
          </a-tag>
          <span v-else class="text-gray-400">未分组</span>
        </template>
        <template #last_connected="{ record }">
          <span v-if="record.last_connected_at">
            {{ formatTime(record.last_connected_at) }}
          </span>
          <span v-else class="text-gray-400">从未连接</span>
        </template>
        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="checkSingleConnectivity(record)" :loading="record.checking">
              <template #icon><icon-sync /></template>
              检测
            </a-button>
            <a-button type="text" size="small" @click="openTerminal(record)">
              <template #icon><icon-desktop /></template>
              SSH 终端
            </a-button>
            <a-button type="text" size="small" @click="showEditServerModal(record)">
              <template #icon><icon-edit /></template>
              编辑
            </a-button>
            <a-popconfirm content="确定要删除此服务器吗？" @ok="handleDeleteServer(record.id)">
              <a-button type="text" status="danger" size="small">
                <template #icon><icon-delete /></template>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 添加/编辑服务器对话框 -->
    <a-modal
      v-model:visible="serverModalVisible"
      :title="editingServer ? '编辑服务器' : '添加服务器'"
      width="600px"
      @ok="handleSaveServer"
      @cancel="closeServerModal"
    >
      <a-form :model="serverForm" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="服务器名称" required>
              <a-input v-model="serverForm.name" placeholder="例如：生产服务器1" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="环境" required>
              <a-select v-model="serverForm.environment" placeholder="选择环境">
                <a-option v-for="env in environments" :key="env.value" :value="env.value">
                  {{ env.label }}
                </a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="主机名/IP" required>
              <a-input v-model="serverForm.hostname" placeholder="例如：192.168.1.100" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="SSH端口">
              <a-input-number v-model="serverForm.port" :min="1" :max="65535" placeholder="22" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="用户名" required>
              <a-input v-model="serverForm.username" placeholder="例如：root" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="操作系统">
              <a-select v-model="serverForm.os_type">
                <a-option value="linux">Linux</a-option>
                <a-option value="windows">Windows</a-option>
                <a-option value="macos">macOS</a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="密码">
          <a-input-password
            v-model="serverForm.password"
            placeholder="SSH 密码（可选）"
            allow-clear
          />
        </a-form-item>

        <a-form-item label="私钥">
          <a-textarea
            v-model="serverForm.private_key"
            placeholder="SSH 私钥（可选，与密码二选一）"
            :auto-size="{ minRows: 3, maxRows: 6 }"
          />
        </a-form-item>

        <a-form-item label="Salt Minion ID">
          <a-input v-model="serverForm.salt_minion_id" placeholder="例如：minion-01" />
        </a-form-item>

        <!-- 测试连通性 -->
        <a-divider>连通性测试</a-divider>
        <a-form-item>
          <a-button 
            type="outline" 
            @click="testServerConnectivity" 
            :loading="testingConnectivity"
            :disabled="!serverForm.hostname || !serverForm.username"
          >
            <template #icon><icon-check-circle /></template>
            测试连接
          </a-button>
          <a-alert v-if="connectivityResult" :type="connectivityResult.is_connected ? 'success' : 'error'" class="mt-2">
            <template #title>
              {{ connectivityResult.is_connected ? '连接成功' : '连接失败' }}
            </template>
            <template #content>
              <div v-if="connectivityResult.is_connected">
                响应时间: {{ connectivityResult.response_time }}ms
              </div>
              <div v-else>
                {{ connectivityResult.error_message }}
              </div>
            </template>
          </a-alert>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- SSH 终端对话框 -->
    <a-modal
      v-model:visible="terminalVisible"
      title="SSH 终端"
      width="80%"
      :footer="false"
      @close="closeTerminal"
    >
      <div style="height: 600px">
        <SSHTerminal
          v-if="currentServer"
          :hostname="currentServer.hostname"
          :port="currentServer.port"
          :username="currentServer.username"
          :password="currentServer.password"
          :connection-id="`ssh-${currentServer.id}`"
          @connected="onTerminalConnected"
          @disconnected="onTerminalDisconnected"
        />
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Message, Modal } from '@arco-design/web-vue'
import {
  IconPlus,
  IconRefresh,
  IconCheckCircle,
  IconCloseCircle,
  IconSearch,
  IconSync,
  IconDesktop,
  IconEdit,
  IconDelete,
} from '@arco-design/web-vue/es/icon'
import {
  getServers,
  createServer,
  updateServer,
  deleteServer,
  checkConnectivity,
  getServerGroups,
  type Server,
  type ServerCreate,
  type ServerUpdate,
  type ServerGroup,
  type ConnectivityCheckResponse,
} from '@/api/server'
import SSHTerminal from '@/components/SSHTerminal.vue'

const environments = [
  { value: 'fuchunyun', label: '富春云环境' },
  { value: 'aliyun', label: '阿里云环境' },
  { value: 'binjiang', label: '滨江环境' },
  { value: 'aliyunyc', label: '阿里云压测环境' },
]

// 搜索和过滤
const searchKeyword = ref('')
const selectedEnvironment = ref('')
const statusFilter = ref<boolean | undefined>(undefined)

// 服务器列表
const loading = ref(false)
const serverList = ref<Server[]>([])
const serverGroups = ref<ServerGroup[]>([])

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: true,
  showPageSize: true,
})

const columns = [
  { title: '服务器名称', dataIndex: 'name', width: 150 },
  { title: '主机名/IP', dataIndex: 'hostname', width: 150 },
  { title: '端口', dataIndex: 'port', width: 80 },
  { title: '用户名', dataIndex: 'username', width: 100 },
  { title: '环境', slotName: 'environment', width: 120 },
  { title: '状态', slotName: 'status', width: 100 },
  { title: '最后连接时间', slotName: 'last_connected', width: 160 },
  { title: '操作', slotName: 'actions', width: 280, fixed: 'right' },
]

// 服务器表单
const serverModalVisible = ref(false)
const editingServer = ref<Server | null>(null)
const serverForm = reactive<Partial<ServerCreate> & { environment?: string }>({
  name: '',
  hostname: '',
  port: 22,
  username: '',
  password: '',
  private_key: '',
  os_type: 'linux',
  environment: undefined,
  salt_minion_id: '',
})

// 连通性测试
const testingConnectivity = ref(false)
const connectivityResult = ref<ConnectivityCheckResponse | null>(null)

// SSH 终端
const terminalVisible = ref(false)
const currentServer = ref<Server | null>(null)

onMounted(() => {
  loadServers()
  loadServerGroups()
})

// ============ 数据加载 ============

async function loadServers() {
  loading.value = true
  try {
    const { data } = await getServers({
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      search: searchKeyword.value || undefined,
      environment: selectedEnvironment.value || undefined,
      status: statusFilter.value,
    })
    serverList.value = data.items || []
    pagination.total = data.total || 0
  } catch (error: any) {
    console.error('加载服务器列表失败:', error)
    Message.error(error.response?.data?.detail || '加载服务器列表失败')
    serverList.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

async function loadServerGroups() {
  try {
    const { data } = await getServerGroups()
    serverGroups.value = data || []
  } catch (error: any) {
    console.error('加载服务器分组失败:', error)
    // 不显示错误消息，因为分组是可选的
    serverGroups.value = []
  }
}

// ============ 搜索和分页 ============

function handleSearch() {
  pagination.current = 1
  loadServers()
}

function resetSearch() {
  searchKeyword.value = ''
  selectedEnvironment.value = ''
  statusFilter.value = undefined
  pagination.current = 1
  loadServers()
}

function handlePageChange(page: number) {
  pagination.current = page
  loadServers()
}

function handlePageSizeChange(pageSize: number) {
  pagination.pageSize = pageSize
  pagination.current = 1
  loadServers()
}

// ============ 服务器 CRUD ============

function showAddServerModal() {
  editingServer.value = null
  resetServerForm()
  serverModalVisible.value = true
}

function showEditServerModal(server: Server) {
  editingServer.value = server
  Object.assign(serverForm, {
    name: server.name,
    hostname: server.hostname,
    port: server.port,
    username: server.username,
    password: '',
    private_key: '',
    os_type: server.os_type,
    environment: server.group?.environment,
    salt_minion_id: server.salt_minion_id,
  })
  serverModalVisible.value = true
}

function closeServerModal() {
  serverModalVisible.value = false
  resetServerForm()
  connectivityResult.value = null
}

function resetServerForm() {
  Object.assign(serverForm, {
    name: '',
    hostname: '',
    port: 22,
    username: '',
    password: '',
    private_key: '',
    os_type: 'linux',
    environment: undefined,
    salt_minion_id: '',
  })
}

async function handleSaveServer() {
  if (!serverForm.name || !serverForm.hostname || !serverForm.username) {
    Message.warning('请填写必填项')
    return
  }

  try {
    if (editingServer.value) {
      await updateServer(editingServer.value.id, serverForm as ServerUpdate)
      Message.success('服务器更新成功')
    } else {
      await createServer(serverForm as ServerCreate)
      Message.success('服务器添加成功')
    }
    closeServerModal()
    loadServers()
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '操作失败')
  }
}

async function handleDeleteServer(serverId: number) {
  try {
    await deleteServer(serverId)
    Message.success('服务器已删除')
    loadServers()
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '删除失败')
  }
}

// ============ 连通性检测 ============

async function testServerConnectivity() {
  if (!serverForm.hostname || !serverForm.username) {
    Message.warning('请先填写主机名和用户名')
    return
  }

  testingConnectivity.value = true
  connectivityResult.value = null

  try {
    // 临时创建一个服务器对象进行测试
    const tempServer: Server = {
      id: 0,
      name: serverForm.name || '临时服务器',
      hostname: serverForm.hostname,
      port: serverForm.port || 22,
      username: serverForm.username,
      os_type: serverForm.os_type || 'linux',
      status: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }

    // TODO: 这里需要调用后端 API 进行连通性测试
    // 由于还没有保存，可以先提示用户
    Message.info('请先保存服务器后再测试连通性')
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '连接测试失败')
  } finally {
    testingConnectivity.value = false
  }
}

async function checkSingleConnectivity(server: Server) {
  server.checking = true
  try {
    const { data } = await checkConnectivity(server.id)
    server.is_connected = data.is_connected
    server.last_connected_at = new Date().toISOString()
    Message.success(data.is_connected ? '服务器在线' : '服务器离线')
    loadServers()
  } catch (error: any) {
    Message.error(error.response?.data?.detail || '检测失败')
  } finally {
    server.checking = false
  }
}

// ============ SSH 终端 ============

function openTerminal(server: Server) {
  if (!server.is_connected) {
    Message.warning('服务器当前离线，无法打开终端')
    return
  }
  currentServer.value = server
  terminalVisible.value = true
}

function closeTerminal() {
  currentServer.value = null
  terminalVisible.value = false
}

function onTerminalConnected() {
  console.log('SSH 终端已连接')
}

function onTerminalDisconnected() {
  console.log('SSH 终端已断开')
}

// ============ 辅助函数 ============

function getEnvironmentLabel(env: string): string {
  const found = environments.find(e => e.value === env)
  return found ? found.label : env
}

function formatTime(timeStr: string): string {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`
  
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.server-management {
  padding: 20px;
}

.search-form {
  margin-bottom: 16px;
  padding: 16px;
  background: #f7f8fa;
  border-radius: 4px;
}

.mt-2 {
  margin-top: 8px;
}

.text-gray-400 {
  color: #a9aeb8;
}
</style>
