# UI/UX 设计规范

详细的视觉设计、交互规范和样式系统。

---

## 🎨 设计原则

### 1. 视觉层次（Visual Hierarchy）
- **重要性分级**：主要操作使用 Primary 按钮，次要操作用 Default，危险操作用 Danger
- **空间留白**：卡片间距 16px，表单元素间距 20-24px，避免拥挤
- **色彩对比**：文字颜色遵循 #1f1f1f（主）→ #595959（次）→ #8c8c8c（辅助）

### 2. 交互反馈（Interaction Feedback）
- **即时反馈**：所有操作必须有 loading 状态或成功/失败提示
- **hover 效果**：按钮、卡片、链接必须有 hover 状态（颜色变化、阴影、微动效）
- **过渡动画**：使用 0.3s 缓动，避免生硬切换

### 3. 一致性（Consistency）
- **组件统一**：相同功能使用相同组件和样式
- **间距系统**：4px 基础单位（4、8、12、16、20、24、32px）
- **圆角规范**：卡片 8-12px，按钮 6-8px，输入框 6-8px

### 4. 响应式（Responsive）
- **断点**：1200px（桌面）、768px（平板）、480px（手机）
- **弹性布局**：优先使用 flex 和 grid，避免固定宽度

---

## 色彩系统

### 主色调
```scss
$primary-color: #667eea;        // 渐变起点
$primary-dark: #4c5ce6;         // 渐变终点
```

### 功能色
```scss
$success-color: #52c41a;        // 成功
$warning-color: #faad14;        // 警告
$error-color: #ff4d4f;          // 错误
$info-color: #1890ff;           // 信息
```

### 中性色
```scss
$text-primary: #1f1f1f;         // 主标题
$text-secondary: #595959;       // 正文
$text-tertiary: #8c8c8c;        // 辅助文字
$border-color: #e8e8e8;         // 边框
$bg-light: #f7f8fa;             // 浅灰背景
$bg-white: #ffffff;             // 白色背景
```

### 常用渐变配色
```scss
// 蓝紫渐变（推荐）
background: linear-gradient(135deg, #667eea 0%, #4c5ce6 100%);

// 青蓝渐变
background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);

// 橙红渐变
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

// 绿青渐变
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
```

---

## 间距系统

基于 4px 基础单位：

```scss
$space-xs: 4px;      // 极小间距
$space-sm: 8px;      // 小间距（按钮间距）
$space-md: 12px;     // 中小间距
$space-base: 16px;   // 标准间距（卡片间距）
$space-lg: 20px;     // 大间距
$space-xl: 24px;     // 超大间距（页面内边距）
$space-2xl: 32px;    // 特大间距
$space-3xl: 40px;    // 极大间距
```

### 应用规则
- 页面内边距：24px
- 卡片间距：16px
- 表单元素间距：20-24px
- 按钮间距：8px（a-space）
- 表格单元格内边距：16px

---

## 阴影规范

### 卡片阴影
```scss
$shadow-card: 0 2px 8px rgba(0, 0, 0, 0.06);
$shadow-card-hover: 0 4px 16px rgba(0, 0, 0, 0.1);
```

### 按钮阴影
```scss
$shadow-button: 0 2px 0 rgba(0, 0, 0, 0.045);
$shadow-button-primary: 0 4px 12px rgba(102, 126, 234, 0.3);
```

### 弹窗阴影
```scss
$shadow-modal: 0 8px 40px rgba(0, 0, 0, 0.12);
```

### 使用示例
```scss
.card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  
  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }
}
```

---

## 动画规范

### 过渡时间
```scss
$duration-fast: 0.15s;   // 快速（小元素）
$duration-base: 0.3s;    // 标准（大部分场景）
$duration-slow: 0.5s;    // 慢速（大元素）
```

### 缓动函数
```scss
$ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
$ease-out: cubic-bezier(0.215, 0.61, 0.355, 1);
```

### 常用动画 Mixin
```scss
@mixin transition-base {
  transition: all $duration-base $ease-in-out;
}

@mixin hover-lift {
  &:hover {
    transform: translateY(-2px);
    box-shadow: $shadow-card-hover;
  }
}
```

### 使用示例
```scss
.button {
  @include transition-base;
  
  &:hover {
    @include hover-lift;
  }
}
```

---

## 页面布局规范

### 标准列表页布局

```
┌─────────────────────────────────────┐
│  面包屑 + 页面标题 + 操作按钮          │  Header
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │  搜索表单（a-card）            │    │  Search
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │  数据表格（a-card + a-table） │    │  Table
│  │                             │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### 表单详情页布局

```
┌─────────────────────────────────────┐
│  面包屑 + 返回按钮 + 页面标题          │  Header
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │  表单内容（a-card + a-form）  │    │  Form
│  │                             │    │
│  │  [取消]  [提交]               │    │  Actions
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### 仪表盘布局

```
┌─────────────────────────────────────┐
│  页面标题 + 时间筛选                   │  Header
├─────────────────────────────────────┤
│  [统计卡片1] [统计卡片2] [统计卡片3]   │  Stats
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐         │
│  │  图表1    │  │  图表2    │         │  Charts
│  └──────────┘  └──────────┘         │
├─────────────────────────────────────┤
│  最新数据表格                         │  Table
└─────────────────────────────────────┘
```

---

## 按钮设计规范

### 视觉层次

```vue
<!-- 主要操作（渐变 + 阴影） -->
<a-button type="primary" class="btn-primary">
  <template #icon><PlusOutlined /></template>
  新增
</a-button>

<!-- 次要操作（描边） -->
<a-button>取消</a-button>

<!-- 危险操作（红色） -->
<a-button type="primary" danger>删除</a-button>

<!-- 链接按钮（表格操作） -->
<a-button type="link" size="small" class="btn-link">编辑</a-button>
```

### 样式增强

```scss
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #4c5ce6 100%);
  border: none;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all 0.3s;
  
  &:hover {
    background: linear-gradient(135deg, #5a6fd6 0%, #3b4bd5 100%);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    transform: translateY(-1px);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.btn-link {
  padding: 0 8px;
  color: #667eea;
  
  &:hover {
    color: #4c5ce6;
    background: rgba(102, 126, 234, 0.06);
  }
}
```

### 使用规则
1. 一个页面只能有一个主要按钮（通常是"新增"或"提交"）
2. 危险操作必须使用 `danger` 属性
3. 表格内操作使用 `link` 类型
4. 所有按钮必须有 hover 效果

---

## 表格设计规范

### 视觉优化

```vue
<a-table
  :columns="columns"
  :data-source="dataSource"
  :loading="loading"
  :pagination="pagination"
  :scroll="{ x: 1200 }"
  row-key="id"
  class="enhanced-table"
  @change="handleTableChange"
>
  <template #bodyCell="{ column, record }">
    <!-- 状态标识 -->
    <template v-if="column.key === 'status'">
      <a-badge
        :status="record.status === 1 ? 'success' : 'error'"
        :text="record.status === 1 ? '启用' : '禁用'"
        class="status-badge"
      />
    </template>
    
    <!-- 标签 -->
    <template v-if="column.key === 'type'">
      <a-tag v-if="record.type === 'admin'" color="blue">管理员</a-tag>
      <a-tag v-else color="green">普通用户</a-tag>
    </template>
    
    <!-- 操作列 -->
    <template v-if="column.key === 'action'">
      <a-space :size="8">
        <a-button type="link" size="small" @click="handleEdit(record)">
          <template #icon><EditOutlined /></template>
          编辑
        </a-button>
        <a-popconfirm title="确定删除？" @confirm="handleDelete(record)">
          <a-button type="link" danger size="small">
            <template #icon><DeleteOutlined /></template>
            删除
          </a-button>
        </a-popconfirm>
      </a-space>
    </template>
  </template>
</a-table>
```

### 表格样式

```scss
.enhanced-table {
  border-radius: 8px;
  overflow: hidden;
  
  :deep(.ant-table-thead > tr > th) {
    background: #fafafa;
    font-weight: 600;
    color: #1f1f1f;
    padding: 16px;
  }
  
  :deep(.ant-table-tbody > tr) {
    transition: background 0.3s;
    
    &:hover {
      background: #f5f7fa;
    }
    
    &:hover > td {
      background: transparent;
    }
  }
  
  :deep(.ant-table-tbody > tr > td) {
    padding: 16px;
    border-bottom: 1px solid #f0f0f0;
  }
}

.status-badge {
  font-weight: 500;
}
```

### 必须遵守的规则
1. 必须包含 `row-key`、`loading`、`pagination`
2. 操作列固定在右侧 - `fixed: 'right'`
3. 设置横向滚动 - `:scroll="{ x: 1200 }"`（列数 > 5 时）
4. 行 hover 必须变色
5. 状态列使用 `a-badge` 或 `a-tag`
6. 操作列按钮使用 `a-space` 包裹

---

## 表单设计规范

### 验证优化

```vue
<a-form-item
  label="用户名"
  name="username"
  :rules="[
    { required: true, message: '请输入用户名' },
    { min: 3, max: 20, message: '长度在 3-20 个字符' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线' }
  ]"
>
  <a-input 
    v-model:value="formData.username" 
    placeholder="请输入用户名"
    :maxlength="20"
    show-count
  />
</a-form-item>
```

### 必须遵守的规则
1. 所有输入框必须有 placeholder
2. 必填项必须有验证规则
3. 提交按钮必须有 loading 状态
4. 弹窗表单宽度不超过 600px
5. 表单 label 宽度统一使用 `span: 6`
6. 输入框支持 `allow-clear`（文本类）

---

## 响应式设计

### 断点定义

```scss
$breakpoint-desktop: 1200px;
$breakpoint-tablet: 768px;
$breakpoint-mobile: 480px;
```

### 响应式示例

```scss
.page-container {
  padding: 24px;
  
  @media (max-width: 768px) {
    padding: 16px;
  }
  
  @media (max-width: 480px) {
    padding: 12px;
  }
}

// 响应式网格
.a-row {
  @media (max-width: 768px) {
    .a-col {
      span: 24; // 移动端占满整行
    }
  }
}
```

---

## 设计资源推荐

### 配色方案
- [Coolors](https://coolors.co/)
- [ColorHunt](https://colorhunt.co/)

### 图标库
- [Ant Design Icons](https://ant.design/components/icon-cn/)
- [IconPark](https://iconpark.oceanengine.com/)

### 插图资源
- [undraw](https://undraw.co/)
- [Storyset](https://storyset.com/)

### 设计灵感
- [Dribbble](https://dribbble.com/)
- [Behance](https://www.behance.net/)
