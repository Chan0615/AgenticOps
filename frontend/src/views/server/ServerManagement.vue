<template>
  <div class="server-management">
    <a-card title="服务器管理" :bordered="false">
      <template #extra>
        <a-space>
          <a-button type="primary" @click="showAddServerModal">
            <template #icon><icon-plus /></template>
            添加服务器
          </a-button>
          <a-button @click="refreshServers">
            <template #icon><icon-refresh /></template>
            刷新
          </a-button>
        </a-space>
      </template>

      <!-- 环境选择 -->
      <a-form layout="inline" class="mb-4">
        <a-form-item label="环境">
          <a-select v-model="selectedEnv" style="width: 200px" @change="loadMinions">
            <a-option v-for="env in environments" :key="env.value" :value="env.value">
              {{ env.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="testPing">
            <template #icon><icon-check-circle /></template>
            测试连接
          </a-button>
        </a-form-item>
      </a-form>

      <!-- Minion 列表 -->
      <a-table
        :columns="columns"
        :data="minionList"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
      >
        <template #status="{ record }">
          <a-tag :color="record.status === 'alive' ? 'green' : 'red'">
            {{ record.status === 'alive' ? '在线' : '离线' }}
          </a-tag>
        </template>
        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="openTerminal(record)">
              SSH 终端
            </a-button>
            <a-button type="text" size="small" @click="runCommand(record)">
              执行命令
            </a-button>
            <a-popconfirm content="确定要删除此服务器吗？" @ok="deleteServer(record.id)">
              <a-button type="text" status="danger" size="small">删除</a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>
    </a-card>

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

    <!-- 执行命令对话框 -->
    <a-modal
      v-model:visible="commandVisible"
      title="执行命令"
      @ok="executeCommand"
      @cancel="commandVisible = false"
    >
      <a-form :model="commandForm" layout="vertical">
        <a-form-item label="命令" required>
          <a-input
            v-model="commandForm.command"
            placeholder="输入要执行的命令，如: uptime, df -h"
            allow-clear
          />
        </a-form-item>
      </a-form>
      
      <!-- 命令执行结果 -->
      <a-alert v-if="commandResult" :type="commandResult.success ? 'success' : 'error'" class="mt-4">
        <template #title>
          {{ commandResult.success ? '执行成功' : '执行失败' }}
        </template>
        <template #content>
          <pre class="command-output">{{ commandResult.output || commandResult.error }}</pre>
        </template>
      </a-alert>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import { IconPlus, IconRefresh, IconCheckCircle } from '@arco-design/web-vue/es/icon'
import { saltGetMinions, saltPing, saltRunCommand } from '@/api/server'
import SSHTerminal from '@/components/SSHTerminal.vue'

const environments = [
  { value: 'fuchunyun', label: '富春云环境' },
  { value: 'aliyun', label: '阿里云环境' },
  { value: 'binjiang', label: '滨江环境' },
  { value: 'aliyunyc', label: '阿里云压测环境' },
]
const selectedEnv = ref('fuchunyun')
const loading = ref(false)
const minionList = ref<any[]>([])

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: true,
  showPageSize: true,
})

const columns = [
  { title: 'Minion ID', dataIndex: 'id' },
  { title: '状态', slotName: 'status' },
  { title: 'IP 地址', dataIndex: 'ip' },
  { title: '操作系统', dataIndex: 'os' },
  { title: '操作', slotName: 'actions', width: 200 },
]

// SSH 终端
const terminalVisible = ref(false)
const currentServer = ref<any>(null)

// 执行命令
const commandVisible = ref(false)
const commandForm = reactive({ command: '' })
const commandResult = ref<any>(null)
const targetServer = ref<any>(null)

onMounted(() => {
  loadMinions()
})

async function loadMinions() {
  loading.value = true
  try {
    const { data } = await saltGetMinions(selectedEnv.value)
    minionList.value = data.data || []
    pagination.total = minionList.value.length
  } catch (error) {
    Message.error('加载 Minion 列表失败')
  } finally {
    loading.value = false
  }
}

async function testPing() {
  loading.value = true
  try {
    const { data } = await saltPing(selectedEnv.value)
    Message.success('Ping 测试完成')
    await loadMinions()
  } catch (error) {
    Message.error('Ping 测试失败')
  } finally {
    loading.value = false
  }
}

function openTerminal(server: any) {
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

function runCommand(server: any) {
  targetServer.value = server
  commandForm.command = ''
  commandResult.value = null
  commandVisible.value = true
}

async function executeCommand() {
  if (!commandForm.command || !targetServer.value) return
  
  loading.value = true
  try {
    const { data } = await saltRunCommand(
      selectedEnv.value,
      targetServer.value.id,
      commandForm.command
    )
    commandResult.value = {
      success: true,
      output: data.data,
    }
    Message.success('命令执行成功')
  } catch (error: any) {
    commandResult.value = {
      success: false,
      error: error.response?.data?.detail || '命令执行失败',
    }
    Message.error('命令执行失败')
  } finally {
    loading.value = false
  }
}

function showAddServerModal() {
  Message.info('添加服务器功能开发中...')
}

function refreshServers() {
  loadMinions()
}

async function deleteServer(id: number) {
  Message.info('删除服务器功能开发中...')
}
</script>

<style scoped>
.server-management {
  padding: 20px;
}

.command-output {
  background: #1e1e1e;
  color: #ffffff;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Menlo, Monaco, "Courier New", monospace';
  font-size: 12px;
  max-height: 300px;
  overflow: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.mb-4 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 16px;
}
</style>
