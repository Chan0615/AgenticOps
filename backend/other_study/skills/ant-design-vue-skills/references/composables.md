# Composables 组合式函数

提供可复用的高级 Composables，简化开发流程。

---

## useLoading - 加载状态管理

自动管理异步操作的 loading 状态，避免手动设置。

### 源代码

```typescript
// src/composables/useLoading.ts
import { ref } from 'vue'

export function useLoading(initialState = false) {
  const loading = ref(initialState)
  
  const setLoading = (value: boolean) => {
    loading.value = value
  }
  
  const withLoading = async <T>(asyncFn: () => Promise<T>): Promise<T> => {
    setLoading(true)
    try {
      return await asyncFn()
    } finally {
      setLoading(false)
    }
  }
  
  return {
    loading,
    setLoading,
    withLoading,
  }
}
```

### 使用示例

```vue
<script setup lang="ts">
import { useLoading } from '@/composables/useLoading'

const { loading, withLoading } = useLoading()

const fetchData = async () => {
  await withLoading(async () => {
    const res = await api.getList()
    dataSource.value = res.data
  })
}

const handleSubmit = async () => {
  await withLoading(async () => {
    await api.create(formData)
    message.success('创建成功')
  })
}
</script>

<template>
  <a-table :loading="loading" />
  <a-button :loading="loading" @click="handleSubmit">提交</a-button>
</template>
```

### 优势
- ✅ 避免手动设置 `loading.value = true/false`
- ✅ 自动处理异常，确保 loading 状态正确重置
- ✅ 支持泛型，保持类型安全
- ✅ 可在任何异步场景使用

---

## usePermission - 权限检查

封装权限判断逻辑，简化代码。

### 源代码

```typescript
// src/composables/usePermission.ts
import { useUserStore } from '@/stores/modules/user'

export function usePermission() {
  const userStore = useUserStore()
  
  const hasPermission = (permission: string): boolean => {
    if (!permission) return true
    
    const permissions = userStore.permissions
    
    // 超级管理员
    if (permissions.includes('*:*:*')) return true
    
    // 精确匹配
    return permissions.includes(permission)
  }
  
  const hasAnyPermission = (permissions: string[]): boolean => {
    return permissions.some(p => hasPermission(p))
  }
  
  const hasAllPermissions = (permissions: string[]): boolean => {
    return permissions.every(p => hasPermission(p))
  }
  
  return {
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
  }
}
```

### 使用示例

```vue
<script setup lang="ts">
import { usePermission } from '@/composables/usePermission'

const { hasPermission, hasAnyPermission } = usePermission()

const canEdit = hasPermission('system:user:edit')
const canDelete = hasPermission('system:user:delete')
const canManage = hasAnyPermission(['system:user:edit', 'system:user:delete'])
</script>

<template>
  <a-button v-if="canEdit">编辑</a-button>
  <a-button v-if="canDelete" danger>删除</a-button>
  
  <!-- 批量权限检查 -->
  <a-dropdown v-if="canManage">
    <a-menu>
      <a-menu-item v-if="hasPermission('system:user:edit')">编辑</a-menu-item>
      <a-menu-item v-if="hasPermission('system:user:delete')">删除</a-menu-item>
    </a-menu>
  </a-dropdown>
</template>
```

### 权限判断方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `hasPermission` | 检查单个权限 | `hasPermission('system:user:add')` |
| `hasAnyPermission` | 检查是否有任一权限 | `hasAnyPermission(['edit', 'delete'])` |
| `hasAllPermissions` | 检查是否拥有所有权限 | `hasAllPermissions(['view', 'edit'])` |

---

## useTable - 表格状态管理

统一管理表格的数据、分页、加载状态。

### 源代码

```typescript
// src/composables/useTable.ts
import { ref, reactive } from 'vue'

export function useTable<T = any>(fetchFn: (params: any) => Promise<any>) {
  const dataSource = ref<T[]>([])
  const loading = ref(false)
  const pagination = reactive({
    current: 1,
    pageSize: 10,
    total: 0,
    showSizeChanger: true,
    showTotal: (total: number) => `共 ${total} 条`,
  })
  
  const fetchData = async () => {
    loading.value = true
    try {
      const res = await fetchFn({
        page: pagination.current,
        pageSize: pagination.pageSize,
      })
      dataSource.value = res.data.list
      pagination.total = res.data.total
    } finally {
      loading.value = false
    }
  }
  
  const handleTableChange = (pag: any) => {
    pagination.current = pag.current
    pagination.pageSize = pag.pageSize
    fetchData()
  }
  
  return {
    dataSource,
    loading,
    pagination,
    fetchData,
    handleTableChange,
  }
}
```

### 使用示例

```vue
<script setup lang="ts">
import { useTable } from '@/composables/useTable'
import { userApi } from '@/api/modules/user'

const {
  dataSource,
  loading,
  pagination,
  fetchData,
  handleTableChange,
} = useTable(userApi.getList)

// 带搜索参数
const searchForm = reactive({ name: '' })

const handleSearch = () => {
  pagination.current = 1
  fetchData()
}

// 修改 fetchData 调用
const fetchDataWithSearch = async () => {
  loading.value = true
  try {
    const res = await userApi.getList({
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

onMounted(() => fetchData())
</script>

<template>
  <a-table
    :columns="columns"
    :data-source="dataSource"
    :loading="loading"
    :pagination="pagination"
    @change="handleTableChange"
  />
</template>
```

### 扩展用法

#### 1. 自定义初始分页
```typescript
const { pagination, fetchData } = useTable(api.getList)

// 修改默认配置
pagination.pageSize = 20
pagination.showSizeChanger = false
```

#### 2. 结合搜索表单
```typescript
const searchForm = reactive({ status: undefined })

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.getList({
      page: pagination.current,
      pageSize: pagination.pageSize,
      ...searchForm, // 合并搜索参数
    })
    dataSource.value = res.data.list
    pagination.total = res.data.total
  } finally {
    loading.value = false
  }
}
```

#### 3. 刷新数据
```typescript
// 保持当前页码
const refresh = () => fetchData()

// 回到第一页
const refreshToFirst = () => {
  pagination.current = 1
  fetchData()
}
```

---

## 何时使用 Composables

### 使用场景对比

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 简单页面（1-2个接口） | 手动管理 | 代码更直观 |
| 复杂页面（3+个接口） | `useLoading` | 避免重复代码 |
| 多个权限判断 | `usePermission` | 集中管理逻辑 |
| 标准列表页 | `useTable` | 统一状态管理 |
| 需要自定义分页逻辑 | 手动管理 | 更灵活 |

### 组合使用示例

```vue
<script setup lang="ts">
import { useLoading } from '@/composables/useLoading'
import { usePermission } from '@/composables/usePermission'

const { loading, withLoading } = useLoading()
const { hasPermission } = usePermission()

// 结合使用
const handleDelete = async (record) => {
  if (!hasPermission('system:user:delete')) {
    message.error('无权限操作')
    return
  }
  
  await withLoading(async () => {
    await api.delete(record.id)
  })
}
</script>
```

---

## 自定义 Composables

如果你的项目有特殊需求，可以基于这些基础 Composables 扩展：

### useExport - 导出功能
```typescript
export function useExport() {
  const exporting = ref(false)
  
  const handleExport = async (fetchFn: () => Promise<any>) => {
    exporting.value = true
    try {
      const data = await fetchFn()
      // 导出逻辑
      message.success('导出成功')
    } finally {
      exporting.value = false
    }
  }
  
  return { exporting, handleExport }
}
```

### useForm - 表单管理
```typescript
export function useForm<T>(initialData: T, rules: any) {
  const formData = reactive<T>({ ...initialData })
  const formRef = ref<FormInstance>()
  
  const reset = () => {
    Object.assign(formData, initialData)
    formRef.value?.resetFields()
  }
  
  const validate = async () => {
    return await formRef.value?.validateFields()
  }
  
  return { formData, formRef, reset, validate }
}
```
