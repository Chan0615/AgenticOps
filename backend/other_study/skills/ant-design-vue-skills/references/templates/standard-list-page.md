# 标准列表页模板

> ✨ **设计亮点**：渐变按钮、hover 动效、圆角卡片、柔和阴影、响应式布局
> 
> 这是最基础的 CRUD 列表页模板，适用于简单的数据管理场景。

## 使用场景
- 简单的数据列表展示
- 基础的新增/编辑/删除功能
- 单条件搜索
- 不需要批量操作

## 完整代码

```vue
<template>
  <div class="page-container">
    <!-- 搜索表单 -->
    <a-card :bordered="false" class="search-card">
      <a-form :model="searchForm" layout="inline">
        <a-form-item label="名称">
          <a-input v-model:value="searchForm.name" placeholder="请输入" allow-clear />
        </a-form-item>
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
      </a-form>
    </a-card>

    <!-- 数据表格 -->
    <a-card :bordered="false" class="table-card">
      <template #title>
        <a-space>
          <a-button type="primary" v-permission="'module:name:add'" @click="handleAdd">
            <template #icon><PlusOutlined /></template>
            新增
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
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-badge
              :status="record.status === 1 ? 'success' : 'error'"
              :text="record.status === 1 ? '启用' : '禁用'"
            />
          </template>
          
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" v-permission="'module:name:edit'" @click="handleEdit(record)">
                编辑
              </a-button>
              <a-popconfirm title="确定删除？" @confirm="handleDelete(record)">
                <a-button type="link" danger size="small" v-permission="'module:name:delete'">
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
        <a-form-item label="名称" name="name">
          <a-input v-model:value="formData.name" placeholder="请输入名称" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import type { FormInstance } from 'ant-design-vue'
import {
  PlusOutlined,
  SearchOutlined,
  ReloadOutlined,
} from '@ant-design/icons-vue'

// 类型定义
interface DataItem {
  id: number
  name: string
  status: number
  createTime: string
}

// 搜索表单
const searchForm = reactive({ name: '' })

// 表格列
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 150, fixed: 'right' },
]

// 表格数据
const dataSource = ref<DataItem[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
})

// 弹窗
const modalVisible = ref(false)
const modalTitle = ref('新增')
const formRef = ref<FormInstance>()
const formData = reactive({ name: '', status: 1 })
const formRules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
}

// 方法
const handleSearch = () => {
  pagination.current = 1
  fetchData()
}

const handleReset = () => {
  Object.assign(searchForm, { name: '' })
  handleSearch()
}

const handleAdd = () => {
  modalTitle.value = '新增'
  Object.assign(formData, { id: undefined, name: '', status: 1 })
  modalVisible.value = true
}

const handleEdit = (record: DataItem) => {
  modalTitle.value = '编辑'
  Object.assign(formData, record)
  modalVisible.value = true
}

const handleDelete = async (record: DataItem) => {
  try {
    message.success('删除成功')
    fetchData()
  } catch (error) {
    message.error('删除失败')
  }
}

const handleModalOk = async () => {
  try {
    await formRef.value?.validateFields()
    message.success(formData.id ? '更新成功' : '新增成功')
    modalVisible.value = false
    fetchData()
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
  loading.value = true
  try {
    // TODO: 调用 API
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchData())
</script>

<style scoped lang="scss">
.page-container {
  padding: 24px;
  background: #f0f2f5;
  min-height: 100vh;

  .search-card {
    margin-bottom: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    
    :deep(.ant-card-body) {
      padding: 24px;
    }
  }

  .table-card {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: box-shadow 0.3s;
    
    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    :deep(.ant-card-head) {
      padding: 0 24px;
      border-bottom: 1px solid #f0f0f0;
    }
    
    :deep(.ant-card-body) {
      padding: 24px;
    }
  }

  // 按钮组样式
  :deep(.ant-btn) {
    border-radius: 6px;
    transition: all 0.3s;
    
    &.ant-btn-primary {
      background: linear-gradient(135deg, #667eea 0%, #4c5ce6 100%);
      border: none;
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
      
      &:hover {
        background: linear-gradient(135deg, #5a6fd6 0%, #3b4bd5 100%);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
      }
      
      &:active {
        transform: translateY(0);
      }
    }
  }

  // 表格样式优化
  :deep(.ant-table) {
    border-radius: 8px;
    overflow: hidden;
    
    .ant-table-thead > tr > th {
      background: #fafafa;
      font-weight: 600;
      color: #1f1f1f;
    }
    
    .ant-table-tbody > tr {
      transition: background 0.3s;
      
      &:hover {
        background: #f5f7fa;
      }
    }
  }
}

// 响应式
@media (max-width: 768px) {
  .page-container {
    padding: 16px;
  }
}
</style>
```

## 关键配置说明

### 必须修改的部分
1. **权限标识**：将 `module:name:add/edit/delete` 替换为实际权限
2. **类型定义**：根据实际数据结构修改 `DataItem`
3. **表格列**：根据业务需求调整 `columns` 配置
4. **表单字段**：根据实际需求修改 `formData` 和 `formRules`
5. **API 调用**：在 `fetchData` 中调用实际接口

### 样式定制
- 修改主色调：替换 `#667eea` 和 `#4c5ce6` 为你的品牌色
- 调整圆角：修改 `border-radius` 值
- 调整阴影：修改 `box-shadow` 值
