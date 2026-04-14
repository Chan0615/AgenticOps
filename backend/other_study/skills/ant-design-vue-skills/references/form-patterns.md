# 表单最佳实践

## 搜索表单

**标准模式**：
- 使用 `a-row` + `a-col` 实现响应式布局
- 每个表单项占 8 列（3 列布局）
- 查询/重置按钮放在最后一个表单项

```vue
<a-form :model="searchForm" layout="inline">
  <a-row :gutter="16">
    <a-col :span="8">
      <a-form-item label="用户名">
        <a-input v-model:value="searchForm.username" allow-clear />
      </a-form-item>
    </a-col>
    <a-col :span="8">
      <a-form-item label="状态">
        <a-select v-model:value="searchForm.status" allow-clear>
          <a-select-option :value="1">启用</a-select-option>
          <a-select-option :value="0">禁用</a-select-option>
        </a-select>
      </a-form-item>
    </a-col>
    <a-col :span="8">
      <a-form-item>
        <a-space>
          <a-button type="primary" @click="handleSearch">查询</a-button>
          <a-button @click="handleReset">重置</a-button>
        </a-space>
      </a-form-item>
    </a-col>
  </a-row>
</a-form>
```

## 编辑表单

**标准模式**：
- 弹窗宽度 600px
- label 占 6 列，input 占 16 列
- 必填项必须有验证规则

```vue
<a-modal v-model:open="visible" title="编辑" width="600px">
  <a-form
    ref="formRef"
    :model="formData"
    :rules="formRules"
    :label-col="{ span: 6 }"
    :wrapper-col="{ span: 16 }"
  >
    <a-form-item label="名称" name="name">
      <a-input v-model:value="formData.name" />
    </a-form-item>
  </a-form>
</a-modal>
```

## 验证规则

```typescript
const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3-20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
}
```

## 异步提交

```typescript
const handleSubmit = async () => {
  try {
    await formRef.value?.validateFields()
    await withLoading(async () => {
      await api.save(formData)
      message.success('保存成功')
      visible.value = false
      fetchData()
    })
  } catch (error) {
    console.error('验证失败:', error)
  }
}
```

## 表单重置

```typescript
const handleReset = () => {
  Object.assign(formData, {
    username: '',
    email: '',
    role: 'user',
  })
  formRef.value?.resetFields()
}
```
