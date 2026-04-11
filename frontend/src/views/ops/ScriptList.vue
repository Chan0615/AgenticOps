<template>
  <div class="script-page ant-illustration-page">
    <Card :bordered="false">
      <Space wrap style="margin-bottom: 16px">
        <Input v-model:value="searchParams.name" placeholder="搜索脚本名称" allow-clear style="width: 220px" @pressEnter="handleSearch" />
        <Select v-model:value="searchParams.script_type" allow-clear placeholder="脚本类型" style="width: 140px">
          <SelectOption value="shell">Shell</SelectOption>
          <SelectOption value="python">Python</SelectOption>
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
        <Button type="primary" @click="openModal()">创建脚本</Button>
      </div>

      <Table :columns="columns" :data-source="scriptList" :loading="loading" :pagination="pagination" row-key="id" @change="handleTableChange">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'script_type'">
            <Tag :color="record.script_type === 'shell' ? 'green' : 'blue'">{{ record.script_type?.toUpperCase() }}</Tag>
          </template>
          <template v-else-if="column.key === 'group_info'">
            {{ record.project_name || '-' }} / {{ record.group_name || '-' }}
          </template>
          <template v-else-if="column.key === 'timeout'">{{ record.timeout }} 秒</template>
          <template v-else-if="column.key === 'created_at'">{{ formatDateTime(record.created_at) }}</template>
          <template v-else-if="column.key === 'actions'">
            <Space>
              <Button type="link" @click="handleView(record)">查看</Button>
              <Button type="link" @click="openDistribute(record)">分发</Button>
              <Button type="link" @click="openModal(record)">编辑</Button>
              <Popconfirm title="确定删除该脚本吗？" @confirm="handleDelete(record.id)">
                <Button type="link" danger>删除</Button>
              </Popconfirm>
            </Space>
          </template>
        </template>
      </Table>
    </Card>

    <Modal v-model:open="modalOpen" :title="isEdit ? '编辑脚本' : '创建脚本'" width="860px" @ok="handleSubmit" @cancel="resetForm">
      <Form :model="formData" layout="vertical">
        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="脚本名称（可选）">
              <Input v-model:value="formData.name" placeholder="留空则自动使用文件名（含扩展名）" />
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem label="脚本类型" required>
              <Select v-model:value="formData.script_type">
                <SelectOption value="shell">Shell</SelectOption>
                <SelectOption value="python">Python</SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

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

        <FormItem :label="isEdit ? '替换脚本文件（可选）' : '上传脚本文件'" :required="!isEdit">
          <Input type="file" @change="onFileInputChange" />
          <div v-if="selectedFileName" class="upload-tip">已选择：{{ selectedFileName }}</div>
          <div v-if="selectedFileName && !isEdit && !formData.name?.trim()" class="upload-tip">
            将自动命名为：{{ inferNameFromFilename(selectedFileName) }}
          </div>
        </FormItem>

        <Row :gutter="16">
          <Col :span="12">
            <FormItem label="超时时间（秒）">
              <InputNumber v-model:value="formData.timeout" :min="1" :max="3600" style="width: 100%" />
            </FormItem>
          </Col>
        </Row>

        <FormItem label="描述">
          <Input v-model:value="formData.description" placeholder="脚本描述信息" />
        </FormItem>
      </Form>
    </Modal>

    <Modal v-model:open="distributeOpen" title="分发脚本" width="720px" @ok="handleDistributeSubmit" @cancel="resetDistributeForm">
      <Form :model="distributeForm" layout="vertical">
        <FormItem label="脚本">
          <Input :value="distributingScript?.name" disabled />
        </FormItem>
        <FormItem label="目标服务器" required>
          <Select v-model:value="distributeForm.server_ids" mode="multiple" placeholder="请选择服务器">
            <SelectOption v-for="item in serverOptions" :key="item.id" :value="item.id">{{ item.name }} ({{ item.hostname }})</SelectOption>
          </Select>
        </FormItem>
        <FormItem label="目标目录" required>
          <Input v-model:value="distributeForm.target_directory" placeholder="例如：/opt/scripts" />
        </FormItem>
        <FormItem label="目标文件名（可选）">
          <Input v-model:value="distributeForm.file_name" placeholder="例如：deploy.sh" />
        </FormItem>
      </Form>
    </Modal>

    <Modal v-model:open="viewOpen" title="脚本详情" width="1200px" :footer="null" wrap-class-name="script-view-modal">
      <Descriptions bordered :column="2">
        <DescriptionsItem label="脚本名称">{{ viewData.name }}</DescriptionsItem>
        <DescriptionsItem label="脚本类型">
          <Tag :color="viewData.script_type === 'shell' ? 'green' : 'blue'">{{ (viewData.script_type || '').toUpperCase() }}</Tag>
        </DescriptionsItem>
        <DescriptionsItem label="项目/分组">{{ viewData.project_name || '-' }} / {{ viewData.group_name || '-' }}</DescriptionsItem>
        <DescriptionsItem label="超时时间">{{ viewData.timeout }} 秒</DescriptionsItem>
        <DescriptionsItem label="创建人">{{ viewData.created_by || '-' }}</DescriptionsItem>
        <DescriptionsItem label="创建时间">{{ formatDateTime(viewData.created_at) }}</DescriptionsItem>
        <DescriptionsItem label="描述" :span="2">{{ viewData.description || '-' }}</DescriptionsItem>
      </Descriptions>
      <Divider>脚本内容</Divider>
      <div class="script-pre-wrap">
        <pre class="script-pre">{{ viewData.content || '暂无脚本内容' }}</pre>
      </div>

      <Divider>版本历史</Divider>
      <Space wrap style="margin-bottom: 12px; width: 100%">
        <Select v-model:value="compareFromVersionId" placeholder="选择起始版本" style="width: 220px" :options="versionSelectOptions" />
        <Select v-model:value="compareToVersionId" placeholder="选择目标版本" style="width: 220px" :options="versionSelectOptions" />
        <Button @click="handleCompareVersions">版本对比</Button>
      </Space>
      <Table
        :columns="versionColumns"
        :data-source="versionList"
        :loading="versionLoading"
        :pagination="false"
        size="small"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'version_no'">v{{ record.version_no }}</template>
          <template v-else-if="column.key === 'created_at'">{{ formatDateTime(record.created_at) }}</template>
          <template v-else-if="column.key === 'actions'">
            <Space>
              <Button type="link" @click="handleViewVersion(record.id)">查看内容</Button>
              <Button type="link" danger @click="openRollbackModal(record.id)">回滚</Button>
            </Space>
          </template>
        </template>
      </Table>
    </Modal>

    <Modal v-model:open="rollbackOpen" title="回滚脚本版本" @ok="handleRollbackConfirm" @cancel="resetRollbackForm">
      <Form layout="vertical">
        <FormItem label="目标版本">
          <Input :value="rollbackTargetLabel" disabled />
        </FormItem>
        <FormItem label="回滚备注">
          <Input.TextArea v-model:value="rollbackNote" :rows="4" placeholder="例如：回滚到稳定版本，修复生产异常" />
        </FormItem>
      </Form>
    </Modal>

    <Modal v-model:open="versionContentOpen" title="版本内容" width="1200px" :footer="null">
      <div class="version-meta">{{ currentVersionTitle }}</div>
      <div class="script-pre-wrap">
        <pre class="script-pre">{{ versionContent || '暂无内容' }}</pre>
      </div>
    </Modal>

    <Modal v-model:open="versionDiffOpen" title="版本对比" width="1200px" :footer="null">
      <div class="version-meta">{{ versionDiffTitle }}</div>
      <div class="script-pre-wrap">
        <pre class="script-pre">{{ versionDiffText || '两个版本内容一致，无差异' }}</pre>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import {
  Button,
  Card,
  Col,
  Descriptions,
  Divider,
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
  compareScriptVersions,
  deleteScript,
  distributeScript,
  getScriptDetail,
  getScriptList,
  getScriptVersionDetail,
  getScriptVersions,
  replaceScriptFile,
  rollbackScriptVersion,
  updateScript,
  uploadScript,
  type ScriptVersion,
} from '@/api/ops/script'
import { getServerList, type Server } from '@/api/ops/server'
import { getGroupList, getProjectList, type OpsGroup, type OpsProject } from '@/api/ops/group'
import { formatDateTime } from '@/utils/datetime'

const FormItem = Form.Item
const SelectOption = Select.Option
const DescriptionsItem = Descriptions.Item

interface Script {
  id: number
  name: string
  project_id?: number
  group_id?: number
  project_name?: string
  group_name?: string
  description?: string
  content?: string
  file_path?: string
  source_file_name?: string
  script_type: string
  timeout: number
  created_by?: string
  created_at: string
  updated_at: string
}

const searchParams = reactive({
  name: '',
  script_type: undefined as string | undefined,
  project_id: undefined as number | undefined,
  group_id: undefined as number | undefined,
})

const projectOptions = ref<OpsProject[]>([])
const groupOptions = ref<OpsGroup[]>([])
const searchGroupOptions = computed(() => {
  if (!searchParams.project_id) return groupOptions.value
  return groupOptions.value.filter((g) => g.project_id === searchParams.project_id)
})
const formGroupOptions = computed(() => {
  if (!formData.project_id) return []
  return groupOptions.value.filter((g) => g.project_id === formData.project_id)
})

const scriptList = ref<Script[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
})

const columns = [
  { title: '脚本名称', dataIndex: 'name', key: 'name', width: 180 },
  { title: '项目/分组', key: 'group_info', width: 220 },
  { title: '类型', key: 'script_type', width: 100 },
  { title: '超时', key: 'timeout', width: 100 },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '创建人', dataIndex: 'created_by', key: 'created_by', width: 100 },
  { title: '创建时间', key: 'created_at', width: 180 },
  { title: '操作', key: 'actions', width: 220, fixed: 'right' as const },
]

const modalOpen = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const selectedUploadFile = ref<File | null>(null)
const selectedFileName = ref('')

const formData = reactive<Partial<Script>>({
  name: '',
  project_id: undefined,
  group_id: undefined,
  script_type: 'shell',
  timeout: 300,
  description: '',
})

const distributeOpen = ref(false)
const distributingScript = ref<Script | null>(null)
const serverOptions = ref<Server[]>([])
const distributeForm = reactive({
  server_ids: [] as number[],
  target_directory: '/root/ChAn',
  file_name: '',
})

const viewOpen = ref(false)
const viewData = ref<Script>({} as Script)
const versionLoading = ref(false)
const versionList = ref<ScriptVersion[]>([])
const compareFromVersionId = ref<number | undefined>()
const compareToVersionId = ref<number | undefined>()
const versionContentOpen = ref(false)
const versionContent = ref('')
const currentVersionTitle = ref('')
const versionDiffOpen = ref(false)
const versionDiffText = ref('')
const versionDiffTitle = ref('')
const rollbackOpen = ref(false)
const rollbackVersionId = ref<number | undefined>()
const rollbackNote = ref('')

const versionColumns = [
  { title: '版本', key: 'version_no', width: 80 },
  { title: '源文件名', dataIndex: 'source_file_name', key: 'source_file_name', width: 180 },
  { title: '备注', dataIndex: 'note', key: 'note' },
  { title: '上传人', dataIndex: 'created_by', key: 'created_by', width: 100 },
  { title: '时间', key: 'created_at', width: 180 },
  { title: '操作', key: 'actions', width: 180 },
]

const versionSelectOptions = computed(() =>
  versionList.value.map((item) => ({
    label: `v${item.version_no} ${item.source_file_name || ''}`,
    value: item.id,
  })),
)

const rollbackTargetLabel = computed(() => {
  const target = versionList.value.find((item) => item.id === rollbackVersionId.value)
  if (!target) return '-'
  return `v${target.version_no} ${target.source_file_name || ''}`
})

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

const loadScripts = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: pagination.current,
      page_size: pagination.pageSize,
    }
    if (searchParams.name) params.name = searchParams.name
    if (searchParams.script_type) params.script_type = searchParams.script_type
    if (searchParams.project_id) params.project_id = searchParams.project_id
    if (searchParams.group_id) params.group_id = searchParams.group_id
    const res = await getScriptList(params)
    scriptList.value = res.data || []
    pagination.total = res.total || 0
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载脚本列表失败')
    scriptList.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.current = 1
  loadScripts()
}

const handleReset = () => {
  searchParams.name = ''
  searchParams.script_type = undefined
  searchParams.project_id = undefined
  searchParams.group_id = undefined
  pagination.current = 1
  loadScripts()
}

const handleSearchProjectChange = () => {
  searchParams.group_id = undefined
}

const handleTableChange = (pageInfo: any) => {
  pagination.current = pageInfo.current
  pagination.pageSize = pageInfo.pageSize
  loadScripts()
}

const openModal = (record?: Script) => {
  if (record) {
    isEdit.value = true
    editingId.value = record.id
    Object.assign(formData, record)
    if (!formData.project_id && formData.group_id) {
      const group = groupOptions.value.find((g) => g.id === formData.group_id)
      formData.project_id = group?.project_id
    }
  } else {
    resetForm()
    isEdit.value = false
  }
  modalOpen.value = true
}

const resetForm = () => {
  modalOpen.value = false
  isEdit.value = false
  editingId.value = null
  formData.name = ''
  formData.project_id = undefined
  formData.group_id = undefined
  formData.script_type = 'shell'
  formData.timeout = 300
  formData.description = ''
  selectedUploadFile.value = null
  selectedFileName.value = ''
}

const handleFormProjectChange = () => {
  formData.group_id = undefined
}

const onFileInputChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] || null
  selectedUploadFile.value = file
  selectedFileName.value = file?.name || ''
}

const inferNameFromFilename = (filename: string) => {
  const normalized = filename.split(/[\\/]/).pop() || filename
  return normalized.trim() || 'script'
}

const handleSubmit = async () => {
  if (!formData.project_id || !formData.group_id) {
    message.warning('请选择项目和分组')
    return
  }
  if (!isEdit.value && !selectedUploadFile.value) {
    message.warning('请上传脚本文件')
    return
  }

  try {
    const trimmedName = formData.name?.trim()
    if (isEdit.value && editingId.value) {
      if (selectedUploadFile.value) {
        const fd = new FormData()
        fd.append('file', selectedUploadFile.value)
        await replaceScriptFile(editingId.value, fd)
      }
      await updateScript(editingId.value, {
        name: trimmedName || undefined,
        project_id: formData.project_id,
        group_id: formData.group_id,
        description: formData.description,
        script_type: formData.script_type,
        timeout: formData.timeout,
      })
      message.success('脚本更新成功')
    } else {
      const fd = new FormData()
      fd.append('file', selectedUploadFile.value as File)
      if (trimmedName) fd.append('name', trimmedName)
      fd.append('project_id', String(formData.project_id))
      fd.append('group_id', String(formData.group_id))
      if (formData.description) fd.append('description', formData.description)
      if (formData.script_type) fd.append('script_type', formData.script_type)
      if (formData.timeout) fd.append('timeout', String(formData.timeout))
      await uploadScript(fd)
      message.success('脚本创建成功')
    }
    resetForm()
    loadScripts()
  } catch (error: any) {
    message.error(error.response?.data?.detail || (isEdit.value ? '脚本更新失败' : '脚本创建失败'))
  }
}

const handleView = async (record: Script) => {
  viewOpen.value = true
  try {
    const detail = await getScriptDetail(record.id)
    viewData.value = detail
    await loadScriptVersions(record.id)
  } catch {
    viewData.value = record
    versionList.value = []
  }
}

const loadScriptVersions = async (scriptId: number) => {
  versionLoading.value = true
  try {
    const res = await getScriptVersions(scriptId)
    versionList.value = res.data || []
    compareFromVersionId.value = versionList.value[1]?.id
    compareToVersionId.value = versionList.value[0]?.id
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载脚本版本失败')
    versionList.value = []
    compareFromVersionId.value = undefined
    compareToVersionId.value = undefined
  } finally {
    versionLoading.value = false
  }
}

const handleViewVersion = async (versionId: number) => {
  if (!viewData.value.id) return
  try {
    const detail = await getScriptVersionDetail(viewData.value.id, versionId)
    currentVersionTitle.value = `v${detail.version_no} · ${detail.source_file_name || '未知文件'} · ${formatDateTime(detail.created_at)}`
    versionContent.value = detail.content || ''
    versionContentOpen.value = true
  } catch (error: any) {
    message.error(error.response?.data?.detail || '获取版本内容失败')
  }
}

const openRollbackModal = (versionId: number) => {
  rollbackVersionId.value = versionId
  rollbackNote.value = ''
  rollbackOpen.value = true
}

const resetRollbackForm = () => {
  rollbackOpen.value = false
  rollbackVersionId.value = undefined
  rollbackNote.value = ''
}

const handleRollbackConfirm = async () => {
  const versionId = rollbackVersionId.value
  if (!versionId) {
    message.warning('请选择要回滚的版本')
    return
  }
  if (!viewData.value.id) return
  try {
    await rollbackScriptVersion(viewData.value.id, {
      version_id: versionId,
      note: rollbackNote.value || undefined,
    })
    message.success('回滚成功')
    resetRollbackForm()
    const detail = await getScriptDetail(viewData.value.id)
    viewData.value = detail
    await loadScriptVersions(viewData.value.id)
    loadScripts()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '回滚失败')
  }
}

const handleCompareVersions = async () => {
  if (!viewData.value.id || !compareFromVersionId.value || !compareToVersionId.value) {
    message.warning('请选择两个版本进行对比')
    return
  }
  if (compareFromVersionId.value === compareToVersionId.value) {
    message.warning('请选择两个不同版本进行对比')
    return
  }
  try {
    const res = await compareScriptVersions(viewData.value.id, compareFromVersionId.value, compareToVersionId.value)
    const fromVersion = versionList.value.find((v) => v.id === compareFromVersionId.value)
    const toVersion = versionList.value.find((v) => v.id === compareToVersionId.value)
    versionDiffTitle.value = `v${fromVersion?.version_no || '-'} -> v${toVersion?.version_no || '-'}`
    versionDiffText.value = res.diff || ''
    versionDiffOpen.value = true
  } catch (error: any) {
    message.error(error.response?.data?.detail || '版本对比失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await deleteScript(id)
    message.success('删除成功')
    loadScripts()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '删除失败')
  }
}

const loadDistributeServers = async () => {
  try {
    const res = await getServerList({ page: 1, page_size: 200 })
    serverOptions.value = res.data || []
  } catch {
    serverOptions.value = []
  }
}

const openDistribute = async (record: Script) => {
  distributingScript.value = record
  distributeForm.server_ids = []
  distributeForm.target_directory = '/root/ChAn'
  distributeForm.file_name = record.source_file_name || `${record.name}${record.script_type === 'python' ? '.py' : '.sh'}`
  distributeOpen.value = true
  await loadDistributeServers()
}

const resetDistributeForm = () => {
  distributeOpen.value = false
  distributingScript.value = null
  distributeForm.server_ids = []
  distributeForm.target_directory = '/root/ChAn'
  distributeForm.file_name = ''
}

const handleDistributeSubmit = async () => {
  if (!distributingScript.value) return
  if (!distributeForm.server_ids.length || !distributeForm.target_directory) {
    message.warning('请填写目标服务器和目标目录')
    return
  }
  try {
    await distributeScript(distributingScript.value.id, {
      server_ids: distributeForm.server_ids,
      target_directory: distributeForm.target_directory,
      file_name: distributeForm.file_name || undefined,
    })
    message.success('脚本分发任务已提交')
    resetDistributeForm()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '脚本分发失败')
  }
}

onMounted(async () => {
  await loadGroupMeta()
  await loadScripts()
})
</script>

<style scoped>
.upload-tip {
  margin-top: 8px;
  color: #64748b;
  font-size: 12px;
}

.script-pre {
  margin: 0;
  padding: 12px;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 8px;
  white-space: pre;
  min-width: max-content;
}

.script-pre-wrap {
  max-height: calc(100vh - 320px);
  overflow: auto;
}

.version-meta {
  margin-bottom: 10px;
  color: #64748b;
  font-size: 12px;
}
</style>
