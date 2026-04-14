# Table 表格

## 基础用法

```vue
<template>
  <a-table
    :columns="columns"
    :data-source="dataSource"
    :loading="loading"
    :pagination="pagination"
    row-key="id"
    @change="handleTableChange"
  />
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface DataItem {
  id: number
  name: string
  status: number
  createTime: string
}

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 150, fixed: 'right' },
]

const dataSource = ref<DataItem[]>([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
})

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
</script>
```

## 自定义单元格

```vue
<template #bodyCell="{ column, record }">
  <!-- 状态列 -->
  <template v-if="column.key === 'status'">
    <a-badge
      :status="record.status === 1 ? 'success' : 'error'"
      :text="record.status === 1 ? '启用' : '禁用'"
    />
  </template>
  
  <!-- 操作列 -->
  <template v-if="column.key === 'action'">
    <a-space>
      <a-button type="link" size="small" @click="handleEdit(record)">
        编辑
      </a-button>
      <a-popconfirm title="确定删除？" @confirm="handleDelete(record)">
        <a-button type="link" danger size="small">删除</a-button>
      </a-popconfirm>
    </a-space>
  </template>
</template>
```

## 行选择

```vue
<template>
  <a-table
    :row-selection="rowSelection"
    :columns="columns"
    :data-source="dataSource"
    row-key="id"
  />
</template>

<script setup lang="ts">
const selectedRowKeys = ref<number[]>([])

const rowSelection = {
  selectedRowKeys: selectedRowKeys,
  onChange: (keys: number[]) => {
    selectedRowKeys.value = keys
  },
}
</script>
```

## 批量操作

```vue
<template>
  <a-button 
    type="primary" 
    danger
    :disabled="selectedRowKeys.length === 0"
    @click="handleBatchDelete"
  >
    批量删除 ({{ selectedRowKeys.length }})
  </a-button>
</template>
```

## 搜索表格完整示例

详见 [SKILL.md](../SKILL.md) 中的标准列表页模板。
