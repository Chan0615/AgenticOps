<template>
  <div class="ops-group-page ant-illustration-page">
    <Card :bordered="false" title="项目与分组管理">
      <Tabs v-model:activeKey="activeTab">
        <TabPane key="projects" tab="项目管理">
          <Space style="margin-bottom: 16px">
            <Input v-model:value="projectSearch" placeholder="搜索项目名称" allow-clear style="width: 240px" @pressEnter="loadProjects" />
            <Button type="primary" @click="loadProjects">搜索</Button>
            <Button @click="resetProjectSearch">重置</Button>
            <Button type="primary" @click="openProjectModal()">新建项目</Button>
          </Space>

          <Table :columns="projectColumns" :data-source="projects" :loading="loadingProjects" :pagination="false" row-key="id">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'created_at'">
                {{ formatDateTime(record.created_at) }}
              </template>
              <template v-else-if="column.key === 'actions'">
                <Space>
                  <Button type="link" @click="openProjectModal(record)">编辑</Button>
                  <Tooltip v-if="isProtectedProject(record)" title="系统默认项目不允许删除">
                    <Button type="link" danger disabled>删除</Button>
                  </Tooltip>
                  <Popconfirm v-else title="确定删除该项目吗？" @confirm="handleDeleteProject(record.id)">
                    <Button type="link" danger>删除</Button>
                  </Popconfirm>
                </Space>
              </template>
            </template>
          </Table>
        </TabPane>

        <TabPane key="groups" tab="分组管理">
          <Space style="margin-bottom: 16px">
            <Select v-model:value="groupSearchProjectId" allow-clear placeholder="按项目筛选" style="width: 220px">
              <SelectOption v-for="item in projects" :key="item.id" :value="item.id">{{ item.name }}</SelectOption>
            </Select>
            <Input v-model:value="groupSearch" placeholder="搜索分组名称" allow-clear style="width: 240px" @pressEnter="loadGroups" />
            <Button type="primary" @click="loadGroups">搜索</Button>
            <Button @click="resetGroupSearch">重置</Button>
            <Button type="primary" @click="openGroupModal()">新建分组</Button>
          </Space>

          <Table :columns="groupColumns" :data-source="groups" :loading="loadingGroups" :pagination="false" row-key="id">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'created_at'">
                {{ formatDateTime(record.created_at) }}
              </template>
              <template v-else-if="column.key === 'actions'">
                <Space>
                  <Button type="link" @click="openGroupModal(record)">编辑</Button>
                  <Tooltip v-if="isProtectedGroup(record)" title="系统默认分组不允许删除">
                    <Button type="link" danger disabled>删除</Button>
                  </Tooltip>
                  <Popconfirm v-else title="确定删除该分组吗？" @confirm="handleDeleteGroup(record.id)">
                    <Button type="link" danger>删除</Button>
                  </Popconfirm>
                </Space>
              </template>
            </template>
          </Table>
        </TabPane>
      </Tabs>
    </Card>

    <Modal v-model:open="projectModalOpen" :title="projectEditId ? '编辑项目' : '新建项目'" @ok="handleSubmitProject" @cancel="resetProjectForm">
      <Form :model="projectForm" layout="vertical">
        <FormItem label="项目名称" required>
          <Input v-model:value="projectForm.name" placeholder="请输入项目名称" />
        </FormItem>
        <FormItem label="项目编码" required>
          <Input v-model:value="projectForm.code" placeholder="例如：payment" :disabled="!!projectEditId" />
        </FormItem>
        <FormItem label="描述">
          <Input v-model:value="projectForm.description" placeholder="项目描述" />
        </FormItem>
      </Form>
    </Modal>

    <Modal v-model:open="groupModalOpen" :title="groupEditId ? '编辑分组' : '新建分组'" @ok="handleSubmitGroup" @cancel="resetGroupForm">
      <Form :model="groupForm" layout="vertical">
        <FormItem label="所属项目" required>
          <Select v-model:value="groupForm.project_id" placeholder="请选择项目">
            <SelectOption v-for="item in projects" :key="item.id" :value="item.id">{{ item.name }}</SelectOption>
          </Select>
        </FormItem>
        <FormItem label="分组名称" required>
          <Input v-model:value="groupForm.name" placeholder="请输入分组名称" />
        </FormItem>
        <FormItem label="描述">
          <Input v-model:value="groupForm.description" placeholder="分组描述" />
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
  Form,
  Input,
  Modal,
  Popconfirm,
  Select,
  Space,
  Table,
  Tabs,
  Tooltip,
  message,
} from 'ant-design-vue'
import {
  createGroup,
  createProject,
  deleteGroup,
  deleteProject,
  getGroupList,
  getProjectList,
  type OpsGroup,
  type OpsProject,
  updateGroup,
  updateProject,
} from '@/api/ops/group'
import { formatDateTime } from '@/utils/datetime'

const FormItem = Form.Item
const SelectOption = Select.Option
const TabPane = Tabs.TabPane

const activeTab = ref('projects')

const loadingProjects = ref(false)
const loadingGroups = ref(false)
const projects = ref<OpsProject[]>([])
const groups = ref<OpsGroup[]>([])
const projectSearch = ref('')
const groupSearch = ref('')
const groupSearchProjectId = ref<number | undefined>(undefined)

const projectColumns = [
  { title: '项目名称', dataIndex: 'name', key: 'name' },
  { title: '项目编码', dataIndex: 'code', key: 'code' },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 180 },
  { title: '操作', key: 'actions', width: 140 },
]

const groupColumns = [
  { title: '分组名称', dataIndex: 'name', key: 'name' },
  { title: '所属项目', dataIndex: 'project_name', key: 'project_name' },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 180 },
  { title: '操作', key: 'actions', width: 140 },
]

const isProtectedProject = (record: OpsProject) => {
  const code = (record.code || '').toLowerCase()
  const name = (record.name || '').toLowerCase()
  const creator = (record.created_by || '').toLowerCase()
  return code === 'default' || name === 'default' || name.includes('默认') || creator === 'system'
}

const isProtectedGroup = (record: OpsGroup) => {
  const name = (record.name || '').toLowerCase()
  const creator = (record.created_by || '').toLowerCase()
  return name === 'default' || name.includes('默认') || creator === 'system'
}

const projectModalOpen = ref(false)
const projectEditId = ref<number | null>(null)
const projectForm = reactive({
  name: '',
  code: '',
  description: '',
})

const groupModalOpen = ref(false)
const groupEditId = ref<number | null>(null)
const groupForm = reactive({
  project_id: undefined as number | undefined,
  name: '',
  description: '',
})

const loadProjects = async () => {
  loadingProjects.value = true
  try {
    const res = await getProjectList({ page: 1, page_size: 200, name: projectSearch.value || undefined })
    projects.value = res.data || []
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载项目失败')
    projects.value = []
  } finally {
    loadingProjects.value = false
  }
}

const loadGroups = async () => {
  loadingGroups.value = true
  try {
    const res = await getGroupList({
      page: 1,
      page_size: 200,
      project_id: groupSearchProjectId.value,
      name: groupSearch.value || undefined,
    })
    groups.value = res.data || []
  } catch (error: any) {
    message.error(error.response?.data?.detail || '加载分组失败')
    groups.value = []
  } finally {
    loadingGroups.value = false
  }
}

const resetProjectSearch = () => {
  projectSearch.value = ''
  loadProjects()
}

const resetGroupSearch = () => {
  groupSearch.value = ''
  groupSearchProjectId.value = undefined
  loadGroups()
}

const openProjectModal = (record?: OpsProject) => {
  if (record) {
    projectEditId.value = record.id
    projectForm.name = record.name
    projectForm.code = record.code
    projectForm.description = record.description || ''
  } else {
    projectEditId.value = null
    projectForm.name = ''
    projectForm.code = ''
    projectForm.description = ''
  }
  projectModalOpen.value = true
}

const resetProjectForm = () => {
  projectModalOpen.value = false
  projectEditId.value = null
  projectForm.name = ''
  projectForm.code = ''
  projectForm.description = ''
}

const handleSubmitProject = async () => {
  if (!projectForm.name.trim() || !projectForm.code.trim()) {
    message.warning('请填写项目名称和编码')
    return
  }
  try {
    if (projectEditId.value) {
      await updateProject(projectEditId.value, {
        name: projectForm.name,
        description: projectForm.description || undefined,
      })
      message.success('项目更新成功')
    } else {
      await createProject({
        name: projectForm.name,
        code: projectForm.code,
        description: projectForm.description || undefined,
      })
      message.success('项目创建成功')
    }
    resetProjectForm()
    await loadProjects()
    await loadGroups()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '项目保存失败')
  }
}

const handleDeleteProject = async (id: number) => {
  const target = projects.value.find((item) => item.id === id)
  if (target && isProtectedProject(target)) {
    message.warning('系统默认项目不允许删除')
    return
  }
  try {
    await deleteProject(id)
    message.success('项目删除成功')
    await loadProjects()
    await loadGroups()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '项目删除失败')
  }
}

const openGroupModal = (record?: OpsGroup) => {
  if (record) {
    groupEditId.value = record.id
    groupForm.project_id = record.project_id
    groupForm.name = record.name
    groupForm.description = record.description || ''
  } else {
    groupEditId.value = null
    groupForm.project_id = undefined
    groupForm.name = ''
    groupForm.description = ''
  }
  groupModalOpen.value = true
}

const resetGroupForm = () => {
  groupModalOpen.value = false
  groupEditId.value = null
  groupForm.project_id = undefined
  groupForm.name = ''
  groupForm.description = ''
}

const handleSubmitGroup = async () => {
  if (!groupForm.project_id || !groupForm.name.trim()) {
    message.warning('请选择项目并填写分组名称')
    return
  }
  try {
    if (groupEditId.value) {
      await updateGroup(groupEditId.value, {
        project_id: groupForm.project_id,
        name: groupForm.name,
        description: groupForm.description || undefined,
      })
      message.success('分组更新成功')
    } else {
      await createGroup({
        project_id: groupForm.project_id,
        name: groupForm.name,
        description: groupForm.description || undefined,
      })
      message.success('分组创建成功')
    }
    resetGroupForm()
    await loadGroups()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '分组保存失败')
  }
}

const handleDeleteGroup = async (id: number) => {
  const target = groups.value.find((item) => item.id === id)
  if (target && isProtectedGroup(target)) {
    message.warning('系统默认分组不允许删除')
    return
  }
  try {
    await deleteGroup(id)
    message.success('分组删除成功')
    await loadGroups()
  } catch (error: any) {
    message.error(error.response?.data?.detail || '分组删除失败')
  }
}

onMounted(async () => {
  await loadProjects()
  await loadGroups()
})
</script>

<style scoped>
.ops-group-page :deep(.ant-input),
.ops-group-page :deep(.ant-input-affix-wrapper),
.ops-group-page :deep(.ant-select-selector) {
  border: 1px solid #d8e3f5 !important;
  box-shadow: none !important;
  border-radius: 10px !important;
}

.ops-group-page :deep(.ant-input-affix-wrapper .ant-input) {
  border: none !important;
  box-shadow: none !important;
}

.ops-group-page :deep(.ant-input:hover),
.ops-group-page :deep(.ant-input-affix-wrapper:hover),
.ops-group-page :deep(.ant-select:not(.ant-select-disabled):hover .ant-select-selector) {
  border-color: #9fb8e8 !important;
}

.ops-group-page :deep(.ant-input:focus),
.ops-group-page :deep(.ant-input-affix-wrapper-focused),
.ops-group-page :deep(.ant-select-focused .ant-select-selector) {
  border-color: #5b8ee6 !important;
  box-shadow: 0 0 0 2px rgba(91, 142, 230, 0.14) !important;
}
</style>
