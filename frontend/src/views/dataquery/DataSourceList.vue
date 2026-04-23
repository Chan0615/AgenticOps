<template>
  <div class="datasource-page">
    <!-- 搜索区域 -->
    <Card :bordered="false">
      <Space wrap style="margin-bottom: 16px">
        <Input v-model:value="searchName" placeholder="搜索数据源名称" allow-clear style="width: 220px" @pressEnter="handleSearch" />
        <Select v-model:value="searchDbType" placeholder="数据库类型" allow-clear style="width: 150px">
          <SelectOption value="mysql">MySQL</SelectOption>
          <SelectOption value="postgresql">PostgreSQL</SelectOption>
        </Select>
        <Select v-model:value="searchStatus" placeholder="状态" allow-clear style="width: 130px">
          <SelectOption value="active">启用</SelectOption>
          <SelectOption value="inactive">禁用</SelectOption>
        </Select>
        <Button type="primary" @click="handleSearch">搜索</Button>
        <Button @click="handleReset">重置</Button>
      </Space>

      <div style="margin-bottom: 16px">
        <Button type="primary" @click="handleCreate">新增数据源</Button>
      </div>

      <Table
        :columns="columns"
        :data-source="dataSource"
        :loading="loading"
        :pagination="pagination"
        :scroll="{ x: 1200 }"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'db_type'">
            <Tag :color="record.db_type === 'mysql' ? 'blue' : 'green'">
              {{ record.db_type === 'mysql' ? 'MySQL' : 'PostgreSQL' }}
            </Tag>
          </template>
          <template v-else-if="column.key === 'status'">
            <Badge :status="record.status === 'active' ? 'success' : 'default'" :text="record.status === 'active' ? '启用' : '禁用'" />
          </template>
          <template v-else-if="column.key === 'is_system_db'">
            <Tag v-if="record.is_system_db" color="orange">系统库</Tag>
            <span v-else style="color: #94a3b8">-</span>
          </template>
          <template v-else-if="column.key === 'connection'">
            <span style="font-size: 12px; color: #64748b">{{ record.host }}:{{ record.port }}/{{ record.database }}</span>
          </template>
          <template v-else-if="column.key === 'action'">
            <Space>
              <Button type="link" size="small" @click="handleTestConnection(record)">测试</Button>
              <Button type="link" size="small" @click="handleSyncMetadata(record)">同步</Button>
              <Button type="link" size="small" @click="handleViewTables(record)">表结构</Button>
              <Button type="link" size="small" @click="handleEdit(record)">编辑</Button>
              <Popconfirm title="确定删除此数据源？" @confirm="handleDelete(record.id)">
                <Button type="link" size="small" danger>删除</Button>
              </Popconfirm>
            </Space>
          </template>
        </template>
      </Table>
    </Card>

    <!-- 新增/编辑弹窗 -->
    <Modal
      v-model:open="formVisible"
      :title="formMode === 'create' ? '新增数据源' : '编辑数据源'"
      :confirm-loading="formSubmitting"
      width="580px"
      @ok="handleFormSubmit"
    >
      <Form ref="formRef" :model="formData" :rules="formRules" layout="vertical" style="margin-top: 16px">
        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="数据源名称" name="name">
              <Input v-model:value="formData.name" placeholder="请输入名称" />
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="数据库类型" name="db_type">
              <Select v-model:value="formData.db_type" placeholder="请选择">
                <SelectOption value="mysql">MySQL</SelectOption>
                <SelectOption value="postgresql">PostgreSQL</SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="16">
          <Col :span="16">
            <FormItem label="主机地址" name="host">
              <Input v-model:value="formData.host" placeholder="如: 192.168.1.100" />
            </FormItem>
          </Col>
          <Col :span="8">
            <FormItem label="端口" name="port">
              <InputNumber v-model:value="formData.port" :min="1" :max="65535" style="width: 100%" placeholder="3306" />
            </FormItem>
          </Col>
        </Row>
        <FormItem label="数据库名" name="database">
          <Input v-model:value="formData.database" placeholder="请输入数据库名" />
        </FormItem>
        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="用户名" name="username">
              <Input v-model:value="formData.username" placeholder="请输入用户名" />
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="密码" :name="formMode === 'create' ? 'password' : undefined">
              <InputPassword v-model:value="formData.password" :placeholder="formMode === 'edit' ? '留空则不修改' : '请输入密码'" />
            </FormItem>
          </Col>
        </Row>
        <FormItem label="描述" name="description">
          <Textarea v-model:value="formData.description" :rows="2" placeholder="可选描述信息" />
        </FormItem>
        <FormItem>
          <Checkbox v-model:checked="formData.is_system_db">标记为系统自身数据库</Checkbox>
        </FormItem>
        <FormItem>
          <Button :loading="testingConnection" @click="handleTestFormConnection">测试连接</Button>
          <span v-if="testResult" :style="{ color: testResult.success ? '#16a34a' : '#dc2626', marginLeft: '12px' }">
            {{ testResult.message }}
          </span>
        </FormItem>
      </Form>
    </Modal>

    <!-- 表结构查看抽屉 -->
    <Drawer
      v-model:open="tableDrawerVisible"
      :title="`表结构 - ${currentDatasource?.name || ''}`"
      :width="720"
      placement="right"
    >
      <div v-if="tablesLoading" style="text-align: center; padding: 48px 0">
        <Spin tip="加载中..." />
      </div>
      <div v-else-if="!tables.length" style="text-align: center; padding: 48px 0; color: #94a3b8">
        暂无表结构数据，请先同步元数据
      </div>
      <Collapse v-else accordion>
        <CollapsePanel v-for="table in tables" :key="table.table_name" :header="table.table_name">
          <template #extra>
            <Tag v-if="table.table_comment" color="blue" style="margin-right: 0">{{ table.table_comment }}</Tag>
          </template>

          <!-- 自定义描述 -->
          <div style="margin-bottom: 12px">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px">
              <span style="font-size: 12px; color: #64748b; font-weight: 500">业务描述</span>
              <Button type="link" size="small" @click="editTableDescription(table)">编辑</Button>
            </div>
            <div v-if="table.custom_description" style="font-size: 13px; color: #334155; background: #f8fafc; padding: 8px; border-radius: 6px">
              {{ table.custom_description }}
            </div>
            <div v-else style="font-size: 12px; color: #94a3b8">未设置（添加描述可提升 AI 查询准确度）</div>
          </div>

          <!-- 字段列表 -->
          <Table
            :columns="fieldColumns"
            :data-source="table.columns || []"
            :pagination="false"
            size="small"
            row-key="name"
          >
            <template #bodyCell="{ column, record: col }">
              <template v-if="column.key === 'is_pk'">
                <Tag v-if="col.is_pk" color="gold">PK</Tag>
              </template>
              <template v-else-if="column.key === 'nullable'">
                {{ col.nullable ? '是' : '否' }}
              </template>
            </template>
          </Table>

          <!-- 样例数据 -->
          <div v-if="table.sample_data?.length" style="margin-top: 12px">
            <div style="font-size: 12px; color: #64748b; font-weight: 500; margin-bottom: 4px">样例数据</div>
            <div style="overflow-x: auto">
              <pre style="font-size: 12px; background: #f8fafc; padding: 8px; border-radius: 6px">{{ JSON.stringify(table.sample_data, null, 2) }}</pre>
            </div>
          </div>
        </CollapsePanel>
      </Collapse>
    </Drawer>

    <!-- 表描述编辑弹窗 -->
    <Modal v-model:open="descModalVisible" title="编辑表业务描述" @ok="handleDescSubmit">
      <p style="font-size: 12px; color: #94a3b8; margin-bottom: 8px">
        添加表的业务描述可以帮助 AI 更准确地理解数据含义，生成更好的 SQL。
      </p>
      <Textarea v-model:value="descForm.description" :rows="4" placeholder="例如：此表存储用户注册信息，包含用户名、邮箱、创建时间等" />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import {
  Badge,
  Button,
  Card,
  Checkbox,
  Col,
  Collapse,
  Drawer,
  Form,
  Input,
  InputNumber,
  Modal,
  Popconfirm,
  Row,
  Select,
  Space,
  Spin,
  Table,
  Tag,
  message,
} from 'ant-design-vue'
import { datasourceApi, type DataSource, type TableMetadata } from '@/api/dataquery'

const FormItem = Form.Item
const SelectOption = Select.Option
const InputPassword = Input.Password
const Textarea = Input.TextArea
const CollapsePanel = Collapse.Panel

// ============ 列表状态 ============
const loading = ref(false)
const dataSource = ref<DataSource[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchName = ref('')
const searchDbType = ref<string | undefined>(undefined)
const searchStatus = ref<string | undefined>(undefined)

const pagination = computed(() => ({
  current: currentPage.value,
  pageSize: pageSize.value,
  total: total.value,
  showTotal: (t: number) => `共 ${t} 条`,
  showSizeChanger: true,
}))

const columns = [
  { title: '名称', dataIndex: 'name', key: 'name', width: 160 },
  { title: '类型', dataIndex: 'db_type', key: 'db_type', width: 100 },
  { title: '连接信息', key: 'connection', width: 250 },
  { title: '系统库', key: 'is_system_db', width: 80, align: 'center' as const },
  { title: '状态', dataIndex: 'status', key: 'status', width: 80 },
  { title: '描述', dataIndex: 'description', key: 'description', ellipsis: true },
  { title: '操作', key: 'action', width: 320, fixed: 'right' as const },
]

const fetchData = async () => {
  loading.value = true
  try {
    const res = await datasourceApi.list({
      page: currentPage.value,
      page_size: pageSize.value,
      name: searchName.value || undefined,
      db_type: searchDbType.value,
      status: searchStatus.value,
    })
    dataSource.value = res.data
    total.value = res.total
  } catch {
    dataSource.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const handleReset = () => {
  searchName.value = ''
  searchDbType.value = undefined
  searchStatus.value = undefined
  handleSearch()
}

const handleTableChange = (pag: any) => {
  currentPage.value = pag.current
  pageSize.value = pag.pageSize
  fetchData()
}

// ============ 新增/编辑 ============
const formVisible = ref(false)
const formSubmitting = ref(false)
const formMode = ref<'create' | 'edit'>('create')
const editingId = ref<number | null>(null)
const formRef = ref()
const testingConnection = ref(false)
const testResult = ref<{ success: boolean; message: string } | null>(null)

const formData = reactive({
  name: '',
  db_type: 'mysql',
  host: '',
  port: 3306 as number,
  database: '',
  username: '',
  password: '',
  description: '',
  is_system_db: false,
})

const formRules = {
  name: [{ required: true, message: '请输入数据源名称' }],
  db_type: [{ required: true, message: '请选择数据库类型' }],
  host: [{ required: true, message: '请输入主机地址' }],
  port: [{ required: true, message: '请输入端口' }],
  database: [{ required: true, message: '请输入数据库名' }],
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码' }],
}

const resetForm = () => {
  formData.name = ''
  formData.db_type = 'mysql'
  formData.host = ''
  formData.port = 3306
  formData.database = ''
  formData.username = ''
  formData.password = ''
  formData.description = ''
  formData.is_system_db = false
  testResult.value = null
}

const handleCreate = () => {
  formMode.value = 'create'
  editingId.value = null
  resetForm()
  formVisible.value = true
}

const handleEdit = (record: DataSource) => {
  formMode.value = 'edit'
  editingId.value = record.id
  formData.name = record.name
  formData.db_type = record.db_type
  formData.host = record.host
  formData.port = record.port
  formData.database = record.database
  formData.username = record.username
  formData.password = ''
  formData.description = record.description || ''
  formData.is_system_db = record.is_system_db
  testResult.value = null
  formVisible.value = true
}

const handleFormSubmit = async () => {
  try {
    await formRef.value?.validateFields()
  } catch {
    return
  }
  formSubmitting.value = true
  try {
    if (formMode.value === 'create') {
      await datasourceApi.create(formData)
      message.success('创建成功')
    } else {
      const updateData: Record<string, any> = { ...formData }
      if (!updateData.password) delete updateData.password
      await datasourceApi.update(editingId.value!, updateData)
      message.success('更新成功')
    }
    formVisible.value = false
    fetchData()
  } finally {
    formSubmitting.value = false
  }
}

const handleDelete = async (id: number) => {
  await datasourceApi.delete(id)
  message.success('删除成功')
  fetchData()
}

// ============ 测试连接 ============
const handleTestConnection = async (record: DataSource) => {
  const hide = message.loading('测试连接中...', 0)
  try {
    const res = await datasourceApi.test(record.id)
    if (res.code === 200) {
      message.success(res.message)
    } else {
      message.error(res.message)
    }
  } finally {
    hide()
  }
}

const handleTestFormConnection = async () => {
  testingConnection.value = true
  testResult.value = null
  try {
    const res = await datasourceApi.testDirect({
      db_type: formData.db_type,
      host: formData.host,
      port: formData.port,
      database: formData.database,
      username: formData.username,
      password: formData.password,
    })
    testResult.value = { success: res.code === 200, message: res.message }
  } catch (err: any) {
    testResult.value = { success: false, message: err?.message || '连接失败' }
  } finally {
    testingConnection.value = false
  }
}

// ============ 同步元数据 ============
const handleSyncMetadata = async (record: DataSource) => {
  const hide = message.loading('正在同步表结构...', 0)
  try {
    const res = await datasourceApi.syncMetadata(record.id)
    message.success(res.message)
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '同步失败')
  } finally {
    hide()
  }
}

// ============ 表结构查看 ============
const tableDrawerVisible = ref(false)
const tablesLoading = ref(false)
const tables = ref<TableMetadata[]>([])
const currentDatasource = ref<DataSource | null>(null)

const fieldColumns = [
  { title: '字段名', dataIndex: 'name', key: 'name', width: 140 },
  { title: '类型', dataIndex: 'type', key: 'type', width: 140 },
  { title: '注释', dataIndex: 'comment', key: 'comment' },
  { title: '主键', key: 'is_pk', width: 60, align: 'center' as const },
  { title: '可空', key: 'nullable', width: 60, align: 'center' as const },
]

const handleViewTables = async (record: DataSource) => {
  currentDatasource.value = record
  tableDrawerVisible.value = true
  tablesLoading.value = true
  try {
    const res = await datasourceApi.getTables(record.id)
    tables.value = res.data || []
  } catch {
    tables.value = []
  } finally {
    tablesLoading.value = false
  }
}

// ============ 表描述编辑 ============
const descModalVisible = ref(false)
const descForm = reactive({ tableName: '', description: '' })

const editTableDescription = (table: TableMetadata) => {
  descForm.tableName = table.table_name
  descForm.description = table.custom_description || ''
  descModalVisible.value = true
}

const handleDescSubmit = async () => {
  if (!currentDatasource.value) return
  try {
    await datasourceApi.updateTableDescription(
      currentDatasource.value.id,
      descForm.tableName,
      descForm.description,
    )
    message.success('描述已更新')
    descModalVisible.value = false
    handleViewTables(currentDatasource.value)
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '更新失败')
  }
}

// ============ 初始化 ============
onMounted(() => {
  fetchData()
})
</script>
