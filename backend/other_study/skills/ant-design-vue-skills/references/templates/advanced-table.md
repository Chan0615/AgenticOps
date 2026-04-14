# 高级搜索表格模板

> 融合 Arco Pro 的表格最佳实践，适用于复杂的数据管理场景。

## 使用场景
- 多条件搜索（3个及以上搜索字段）
- 需要批量操作（批量删除、批量导出等）
- 需要行选择功能
- 复杂的状态展示（标签、徽章等）
- 需要横向滚动（列数较多）

## 完整代码

```vue
<template>
  <div class="page-container">
    <!-- 面包屑 -->
    <a-breadcrumb class="breadcrumb">
      <a-breadcrumb-item>首页</a-breadcrumb-item>
      <a-breadcrumb-item>系统管理</a-breadcrumb-item>
      <a-breadcrumb-item>用户管理</a-breadcrumb-item>
    </a-breadcrumb>

    <!-- 搜索表单 -->
    <a-card :bordered="false" class="search-card">
      <a-form :model="searchForm" layout="inline">
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="用户名" name="username">
              <a-input 
                v-model:value="searchForm.username" 
                placeholder="请输入用户名"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="状态" name="status">
              <a-select 
                v-model:value="searchForm.status" 
                placeholder="请选择状态"
                allow-clear
              >
                <a-select-option :value="1">启用</a-select-option>
                <a-select-option :value="0">禁用</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item>
              <a-space>
                <a-button type="primary" @click="handleSearch">
                  <template #icon><SearchOutlined /></template>
                  查询
                </a-button>
                <a-button @click="handleReset">
                  <template #icon><ReloadOutlined /></template>
                  重置
                </a-button>
              </a-space>
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-card>

    <!-- 数据表格 -->
    <a-card :bordered="false" class="table-card">
      <template #title>
        <a-space>
          <a-button type="primary" v-permission="'system:user:add'" @click="handleAdd">
            <template #icon><PlusOutlined /></template>
            新增
          </a-button>
          <a-button 
            v-permission="'system:user:batchDelete'"
            danger
            :disabled="selectedRowKeys.length === 0"
            @click="handleBatchDelete"
          >
            <template #icon><DeleteOutlined /></template>
            批量删除 ({{ selectedRowKeys.length }})
          </a-button>
          <a-button @click="handleRefresh">
            <template #icon><ReloadOutlined /></template>
            刷新
          </a-button>
        </a-space>
      </template>

      <a-table
        :columns="columns"
        :data-source="dataSource"
        :loading="loading"
        :pagination="pagination"
        :row-selection="rowSelection"
        :scroll="{ x: 1200 }"
        row-key="id"
        class="enhanced-table"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <!-- 状态列 -->
          <template v-if="column.key === 'status'">
            <a-badge
              :status="record.status === 1 ? 'success' : 'error'"
              :text="record.status === 1 ? '启用' : '禁用'"
            />
          </template>
          
          <!-- 角色列 -->
          <template v-if="column.key === 'role'">
            <a-tag v-if="record.role === 'admin'" color="blue">管理员</a-tag>
            <a-tag v-else-if="record.role === 'editor'" color="green">编辑</a-tag>
            <a-tag v-else color="default">普通用户</a-tag>
          </template>
          
          <!-- 操作列 -->
          <template v-if="column.key === 'action'">
            <a-space :size="8">
              <a-button 
                type="link" 
                size="small"
                v-permission="'system:user:edit'"
                @click="handleEdit(record)"
              >
                <template #icon><EditOutlined /></template>
                编辑
              </a-button>
              <a-popconfirm 
                title="确定删除此用户吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="handleDelete(record)"
              >
                <a-button 
                  type="link" 
                  danger 
                  size="small"
                  v-permission="'system:user:delete'"
                >
                  <template #icon><DeleteOutlined /></template>
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 编辑弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      width="600px"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="用户名" name="username">
          <a-input v-model:value="formData.username" placeholder="请输入用户名" />
        </a-form-item>
        <a-form-item label="邮箱" name="email">
          <a-input v-model:value="formData.email" placeholder="请输入邮箱" />
        </a-form-item>
        <a-form-item label="角色" name="role">
          <a-select v-model:value="formData.role" placeholder="请选择角色">
            <a-select-option value="admin">管理员</a-select-option>
            <a-select-option value="editor">编辑</a-select-option>
            <a-select-option value="user">普通用户</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import type { FormInstance } from 'ant-design-vue'
import {
  PlusOutlined,
  SearchOutlined,
  ReloadOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons-vue'
import { useLoading } from '@/composables/useLoading'
import { userApi } from '@/api/modules/user'

// 类型定义
interface UserItem {
  id: number
  username: string
  email: string
  role: string
  status: number
  createTime: string
}

// 使用 composable
const { loading, withLoading } = useLoading()

// 搜索表单
const searchForm = reactive({
  username: '',
  status: undefined as number | undefined,
})

// 表格列
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '角色', dataIndex: 'role', key: 'role', width: 120 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 200, fixed: 'right' },
]

// 表格数据
const dataSource = ref<UserItem[]>([])
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
})

// 行选择
const selectedRowKeys = ref<number[]>([])
const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys: number[]) => {
    selectedRowKeys.value = keys
  },
}))

// 弹窗
const modalVisible = ref(false)
const modalTitle = ref('新增用户')
const formRef = ref<FormInstance>()
const formData = reactive({
  username: '',
  email: '',
  role: 'user',
})
const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3-20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' },
  ],
}

// 方法
const handleSearch = () => {
  pagination.current = 1
  fetchData()
}

const handleReset = () => {
  Object.assign(searchForm, { username: '', status: undefined })
  handleSearch()
}

const handleAdd = () => {
  modalTitle.value = '新增用户'
  Object.assign(formData, { id: undefined, username: '', email: '', role: 'user' })
  modalVisible.value = true
}

const handleEdit = (record: UserItem) => {
  modalTitle.value = '编辑用户'
  Object.assign(formData, record)
  modalVisible.value = true
}

const handleDelete = async (record: UserItem) => {
  await withLoading(async () => {
    await userApi.delete(record.id)
    message.success('删除成功')
    fetchData()
  })
}

const handleBatchDelete = async () => {
  if (selectedRowKeys.value.length === 0) {
    message.warning('请选择要删除的数据')
    return
  }
  
  Modal.confirm({
    title: '批量删除',
    content: `确定要删除选中的 ${selectedRowKeys.value.length} 条数据吗？`,
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      await withLoading(async () => {
        await userApi.batchDelete(selectedRowKeys.value)
        message.success('批量删除成功')
        selectedRowKeys.value = []
        fetchData()
      })
    },
  })
}

const handleModalOk = async () => {
  try {
    await formRef.value?.validateFields()
    await withLoading(async () => {
      if (formData.id) {
        await userApi.update(formData.id, formData)
        message.success('更新成功')
      } else {
        await userApi.create(formData)
        message.success('新增成功')
      }
      modalVisible.value = false
      fetchData()
    })
  } catch (error) {
    console.error('验证失败:', error)
  }
}

const handleModalCancel = () => {
  modalVisible.value = false
  formRef.value?.resetFields()
}

const handleRefresh = () => fetchData()

const handleTableChange = (pag: any) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchData()
}

const fetchData = async () => {
  await withLoading(async () => {
    const res = await userApi.getList({
      page: pagination.current,
      pageSize: pagination.pageSize,
      ...searchForm,
    })
    dataSource.value = res.data.list
    pagination.total = res.data.total
  })
}

onMounted(() => fetchData())
</script>

<style scoped lang="scss">
.page-container {
  padding: 24px;
  background: #f0f2f5;
  min-height: 100vh;

  .breadcrumb {
    margin-bottom: 16px;
  }

  .search-card {
    margin-bottom: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  .table-card {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  .enhanced-table {
    border-radius: 8px;
    overflow: hidden;
  }
}
</style>
```

## 关键特性

### 1. 行选择功能
```typescript
const selectedRowKeys = ref<number[]>([])
const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys: number[]) => {
    selectedRowKeys.value = keys
  },
}))
```

### 2. 批量操作
```typescript
const handleBatchDelete = async () => {
  Modal.confirm({
    title: '批量删除',
    content: `确定要删除选中的 ${selectedRowKeys.value.length} 条数据吗？`,
    onOk: async () => {
      await userApi.batchDelete(selectedRowKeys.value)
    },
  })
}
```

### 3. 使用 Composable
```typescript
const { loading, withLoading } = useLoading()

// 自动管理 loading 状态
const fetchData = async () => {
  await withLoading(async () => {
    const res = await userApi.getList(params)
  })
}
```

## 与标准模板的区别

| 特性 | 标准模板 | 高级模板 |
|------|---------|---------|
| 搜索字段 | 1-2个 | 3个及以上 |
| 批量操作 | ❌ | ✅ |
| 行选择 | ❌ | ✅ |
| 面包屑 | ❌ | ✅ |
| Composable | 手动管理 | 使用 useLoading |
| 响应式布局 | 简单 | 使用 a-row/a-col |
