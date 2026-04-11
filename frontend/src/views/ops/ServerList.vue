<template>
  <div class="server-page ant-illustration-page">
    <Card :bordered="false">
      <Space wrap style="margin-bottom: 16px">
        <Input v-model:value="searchParams.name" placeholder="搜索服务器名称" allow-clear style="width: 220px" @pressEnter="handleSearch" />
        <Select v-model:value="searchParams.environment" allow-clear placeholder="环境" style="width: 150px">
          <SelectOption value="fuchunyun">富春云</SelectOption>
          <SelectOption value="aliyun">阿里云</SelectOption>
          <SelectOption value="binjiang">滨江</SelectOption>
          <SelectOption value="aliyunyc">阿里云压测</SelectOption>
        </Select>
        <Select v-model:value="searchParams.status" allow-clear placeholder="状态" style="width: 130px">
          <SelectOption value="online">在线</SelectOption>
          <SelectOption value="offline">离线</SelectOption>
          <SelectOption value="unknown">未知</SelectOption>
        </Select>
        <Button type="primary" @click="handleSearch">搜索</Button>
        <Button @click="handleReset">重置</Button>
      </Space>

      <div style="margin-bottom: 16px">
        <Button type="primary" @click="openModal()">添加服务器</Button>
      </div>

      <Table :columns="columns" :data-source="serverList" :loading="loading" :pagination="pagination" row-key="id" @change="handleTableChange">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <Tag :color="getStatusColor(record.status)">{{ getStatusText(record.status) }}</Tag>
          </template>
          <template v-else-if="column.key === 'environment'">
            <Tag :color="getEnvColor(record.environment)">{{ getEnvText(record.environment) }}</Tag>
          </template>
          <template v-else-if="column.key === 'created_at'">{{ formatDateTime(record.created_at) }}</template>
          <template v-else-if="column.key === 'actions'">
            <Space>
              <Button type="link" @click="handleTest(record)">测试连接</Button>
              <Button type="link" @click="openModal(record)">编辑</Button>
              <Popconfirm title="确定要删除该服务器吗？" @confirm="handleDelete(record.id)">
                <Button type="link" danger>删除</Button>
              </Popconfirm>
            </Space>
          </template>
        </template>
      </Table>
    </Card>

    <Modal v-model:open="modalOpen" :title="isEdit ? '编辑服务器' : '添加服务器'" width="720px" @ok="handleSubmit" @cancel="resetForm">
      <Form :model="formData" layout="vertical">
        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="服务器名称" required>
              <Input v-model:value="formData.name" placeholder="例如：生产服务器-01" />
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="IP地址/域名" required>
              <Input v-model:value="formData.hostname" placeholder="例如：192.168.1.100" />
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="16">
          <Col :span="8">
            <FormItem label="SSH端口">
              <InputNumber v-model:value="formData.port" :min="1" :max="65535" style="width: 100%" />
            </FormItem>
          </Col>
          <Col :span="16">
            <FormItem label="登录用户名">
              <Input v-model:value="formData.username" placeholder="root" />
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="环境">
              <Select v-model:value="formData.environment" placeholder="请选择环境">
                <SelectOption value="fuchunyun">富春云</SelectOption>
                <SelectOption value="aliyun">阿里云</SelectOption>
                <SelectOption value="binjiang">滨江</SelectOption>
                <SelectOption value="aliyunyc">阿里云压测</SelectOption>
              </Select>
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="Salt Minion ID">
              <Input v-model:value="formData.salt_minion_id" placeholder="可选" />
            </FormItem>
          </Col>
        </Row>

        <FormItem label="描述">
          <Input.TextArea v-model:value="formData.description" :rows="3" placeholder="服务器描述信息" />
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import {
  Button,
  Card,
  Col,
  Form,
  Input,
  InputNumber,
  Modal,
  Popconfirm,
  Row,
  Select,
  Space,
  Table,
  Tag,
  message,
} from 'ant-design-vue'
import {
  createServer,
  deleteServer,
  getServerList,
  testServerConnection,
  type Server,
  updateServer,
} from '@/api/ops/server'
import { formatDateTime } from '@/utils/datetime'

const FormItem = Form.Item
const SelectOption = Select.Option

const searchParams = reactive({
  name: '',
  environment: undefined as string | undefined,
  status: undefined as string | undefined,
})

const serverList = ref<Server[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
})

const columns = [
  { title: '主机', dataIndex: 'name', key: 'name', width: 150 },
  { title: 'IP', dataIndex: 'hostname', key: 'hostname', width: 130 },
  { title: '端口', dataIndex: 'port', key: 'port', width: 70 },
  { title: '用户', dataIndex: 'username', key: 'username', width: 90 },
  { title: '环境', key: 'environment', width: 110 },
  { title: '状态', key: 'status', width: 90 },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '创建', key: 'created_at', width: 180 },
  { title: '操作', key: 'actions', width: 220, fixed: 'right' as const },
]

const modalOpen = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)

const formData = reactive<Partial<Server>>({
  name: '',
  hostname: '',
  port: 22,
  username: 'root',
  environment: 'fuchunyun',
  salt_minion_id: '',
  description: '',
})

const loadServers = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (searchParams.name) params.name = searchParams.name
    if (searchParams.environment) params.environment = searchParams.environment
    if (searchParams.status) params.status = searchParams.status
    const res = await getServerList(params)
    serverList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载服务器列表失败')
    serverList.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.current = 1
  loadServers()
}

const handleReset = () => {
  searchParams.name = ''
  searchParams.environment = undefined
  searchParams.status = undefined
  pagination.current = 1
  loadServers()
}

const handleTableChange = (pageInfo: any) => {
  pagination.current = pageInfo.current
  pagination.pageSize = pageInfo.pageSize
  loadServers()
}

const openModal = (record?: Server) => {
  if (record) {
    isEdit.value = true
    editingId.value = record.id
    Object.assign(formData, record)
  } else {
    resetForm()
  }
  modalOpen.value = true
}

const handleDelete = async (id: number) => {
  try {
    await deleteServer(id)
    message.success('删除成功')
    loadServers()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '删除失败')
  }
}

const handleTest = async (record: Server) => {
  try {
    const res = await testServerConnection({ server_id: record.id, test_type: 'salt' })
    if (res.code === 200) {
      message.success('连接测试成功')
      loadServers()
    } else {
      message.error(res.message || '连接测试失败')
    }
  } catch (error: any) {
    message.error(error.response?.data?.detail || '连接测试失败')
  }
}

const handleSubmit = async () => {
  if (!formData.name || !formData.hostname) {
    message.warning('请填写服务器名称和IP地址')
    return
  }
  try {
    if (isEdit.value && editingId.value) {
      await updateServer(editingId.value, formData)
      message.success('更新成功')
    } else {
      await createServer(formData)
      message.success('创建成功')
    }
    resetForm()
    loadServers()
  } catch (error: any) {
    message.error(error.response?.data?.detail || (isEdit.value ? '更新失败' : '创建失败'))
  }
}

const resetForm = () => {
  modalOpen.value = false
  isEdit.value = false
  editingId.value = null
  formData.name = ''
  formData.hostname = ''
  formData.port = 22
  formData.username = 'root'
  formData.environment = 'fuchunyun'
  formData.salt_minion_id = ''
  formData.description = ''
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    online: 'green',
    offline: 'red',
    unknown: 'default',
  }
  return colors[status] || 'default'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    online: '在线',
    offline: '离线',
    unknown: '未知',
  }
  return texts[status] || status
}

const getEnvColor = (env: string) => {
  const colors: Record<string, string> = {
    fuchunyun: 'blue',
    aliyun: 'orange',
    binjiang: 'green',
    aliyunyc: 'purple',
  }
  return colors[env] || 'default'
}

const getEnvText = (env: string) => {
  const texts: Record<string, string> = {
    fuchunyun: '富春云',
    aliyun: '阿里云',
    binjiang: '滨江',
    aliyunyc: '阿里云压测',
  }
  return texts[env] || env
}

onMounted(() => {
  loadServers()
})
</script>
