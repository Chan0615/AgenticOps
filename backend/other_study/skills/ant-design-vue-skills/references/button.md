# Button 按钮

## 基础用法

```vue
<template>
  <a-space>
    <a-button type="primary">主要按钮</a-button>
    <a-button>默认按钮</a-button>
    <a-button type="dashed">虚线按钮</a-button>
    <a-button type="text">文本按钮</a-button>
    <a-button type="link">链接按钮</a-button>
  </a-space>
</template>
```

## 按钮类型

| 类型 | 说明 | 使用场景 |
|------|------|---------|
| `primary` | 主要按钮 | 表单提交、主要操作 |
| `default` | 默认按钮 | 次要操作 |
| `dashed` | 虚线按钮 | 添加操作 |
| `text` | 文本按钮 | 轻量级操作 |
| `link` | 链接按钮 | 表格操作列 |

## 危险按钮

```vue
<a-button type="primary" danger>删除</a-button>
<a-button danger>危险操作</a-button>
```

## 带图标按钮

```vue
<template>
  <a-button type="primary">
    <template #icon><PlusOutlined /></template>
    新增
  </a-button>
  
  <a-button>
    <template #icon><SearchOutlined /></template>
    查询
  </a-button>
</template>

<script setup lang="ts">
import { PlusOutlined, SearchOutlined } from '@ant-design/icons-vue'
</script>
```

## 加载状态

```vue
<a-button type="primary" :loading="loading">
  提交
</a-button>
```

## 禁用状态

```vue
<a-button disabled>禁用按钮</a-button>

<!-- 批量操作 -->
<a-button 
  type="primary" 
  danger
  :disabled="selectedRowKeys.length === 0"
>
  批量删除
</a-button>
```

## 表格操作列示例

```vue
<template #bodyCell="{ column, record }">
  <template v-if="column.key === 'action'">
    <a-space>
      <a-button 
        type="link" 
        size="small"
        v-permission="'module:item:edit'"
        @click="handleEdit(record)"
      >
        编辑
      </a-button>
      <a-popconfirm title="确定删除？" @confirm="handleDelete(record)">
        <a-button 
          type="link" 
          danger 
          size="small"
          v-permission="'module:item:delete'"
        >
          删除
        </a-button>
      </a-popconfirm>
    </a-space>
  </template>
</template>
```

## 权限控制

```vue
<!-- 基础用法 -->
<a-button v-permission="'system:user:add'">新增</a-button>

<!-- 配合其他属性 -->
<a-button 
  v-permission="'system:user:batchDelete'"
  type="primary"
  danger
  :disabled="selectedRowKeys.length === 0"
  @click="handleBatchDelete"
>
  批量删除
</a-button>
```
