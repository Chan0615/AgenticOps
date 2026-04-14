# 表格最佳实践

## 标准搜索表格

**页面结构**：
1. 面包屑导航
2. 搜索表单
3. 操作按钮区
4. 数据表格
5. 分页

## 列定义

```typescript
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '角色', dataIndex: 'role', key: 'role', width: 120 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 200, fixed: 'right' },
]
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
  
  <!-- 标签列 -->
  <template v-if="column.key === 'role'">
    <a-tag v-if="record.role === 'admin'" color="blue">管理员</a-tag>
    <a-tag v-else color="default">普通用户</a-tag>
  </template>
  
  <!-- 操作列 -->
  <template v-if="column.key === 'action'">
    <a-space :size="8">
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

```typescript
const selectedRowKeys = ref<number[]>([])
const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys: number[]) => {
    selectedRowKeys.value = keys
  },
}))
```

## 批量操作

```vue
<a-button 
  danger
  :disabled="selectedRowKeys.length === 0"
  @click="handleBatchDelete"
>
  批量删除 ({{ selectedRowKeys.length }})
</a-button>
```

```typescript
const handleBatchDelete = () => {
  Modal.confirm({
    title: '批量删除',
    content: `确定要删除选中的 ${selectedRowKeys.value.length} 条数据吗？`,
    onOk: async () => {
      await api.batchDelete(selectedRowKeys.value)
      message.success('删除成功')
      selectedRowKeys.value = []
      fetchData()
    },
  })
}
```

## 远程数据

```typescript
const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.getList({
      page: pagination.current,
      pageSize: pagination.pageSize,
      ...searchForm,
    })
    dataSource.value = res.data.list
    pagination.total = res.data.total
  } finally {
    loading.value = false
  }
}
```

## 分页配置

```typescript
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条`,
  pageSizeOptions: ['10', '20', '50', '100'],
})
```

## 表格样式

```scss
.enhanced-table {
  border-radius: 8px;
  overflow: hidden;
  
  :deep(.ant-table-thead > tr > th) {
    background: #fafafa;
    font-weight: 600;
  }
  
  :deep(.ant-table-tbody > tr:hover) {
    background: #f5f7fa;
  }
}
```

## 质量检查清单

- [ ] 重置功能恢复筛选条件并重新加载表格
- [ ] 行操作符合权限规则
- [ ] 分页在筛选条件变化后保持稳定
- [ ] 请求参数从一个明显的地方派生
- [ ] 删除操作有二次确认
- [ ] 操作列固定在右侧
