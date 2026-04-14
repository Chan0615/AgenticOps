---
name: ant-design-vue-skills
description: "基于 Ant Design Vue 4.x + Vue 3 + TypeScript + Vite 的企业级后台管理系统完整开发模板和规范。Use this skill whenever the user asks to build an Ant Design Vue project, create enterprise admin system, backend management system, operations platform, add new menu, new module, new page, develop CRUD pages, implement button-level permissions, LDAP login, user management, role management, menu management, dashboard, data table, form page, or any enterprise backend development. Provides complete project structure, 4-step development workflow, standard code templates, permission system, UI/UX specifications, design principles, visual guidelines, and production-ready components. Make sure to use this skill whenever the user mentions Ant Design Vue, a-button, a-table, a-form, enterprise admin, backend management, CRUD operations, permission control, role-based access, or wants to create any Vue 3 admin interface."
---

# Ant Design Vue 企业平台开发 Skill

> 融合现代设计理念的企业级后台开发规范，注重视觉品质、用户体验和交互细节

---

## 📋 快速导航

本 Skill 采用分层结构，根据需求快速定位：

| 你需要 | 查看文件 |
|--------|---------|
| 🚀 快速开始开发新页面 | 继续阅读下方「标准开发流程」 |
| 📄 标准列表页模板 | [references/templates/standard-list-page.md](references/templates/standard-list-page.md) |
| 📊 高级搜索表格 | [references/templates/advanced-table.md](references/templates/advanced-table.md) |
| 🎨 完整 UI/UX 设计规范 | [references/design-system.md](references/design-system.md) |
| 🔧 Composables 使用指南 | [references/composables.md](references/composables.md) |

---

## 🎯 核心设计原则

### 视觉层次
- **重要性分级**：Primary（主要）→ Default（次要）→ Danger（危险）
- **空间留白**：卡片间距 16px，表单元素间距 20-24px
- **色彩对比**：#1f1f1f（主）→ #595959（次）→ #8c8c8c（辅助）

### 交互反馈
- **即时反馈**：所有操作必须有 loading 或成功/失败提示
- **hover 效果**：按钮、卡片必须有 hover 状态
- **过渡动画**：0.3s 缓动，避免生硬切换

### 一致性
- **间距系统**：4px 基础单位（4/8/12/16/20/24/32px）
- **圆角规范**：卡片 8-12px，按钮 6-8px

---

## 🚀 标准开发流程（4步法）

### Step 1: 创建页面文件

**位置**: `src/views/模块名/页面名/index.vue`

根据场景选择模板：
- **简单 CRUD**（1-2个搜索字段，无批量操作）→ 使用[标准列表页模板](references/templates/standard-list-page.md)
- **复杂管理**（3+搜索字段，批量操作，行选择）→ 使用[高级搜索表格](references/templates/advanced-table.md)

**关键要点**：
```vue
<!-- 必须包含的基础结构 -->
<a-card class="search-card">搜索表单</a-card>
<a-card class="table-card">
  <a-table :loading="loading" :pagination="pagination" row-key="id" />
</a-card>
<a-modal>编辑表单</a-modal>
```

### Step 2: 添加路由配置

**位置**: `src/router/index.ts`

```typescript
{
  path: '/system/user',
  name: 'SystemUser',
  component: () => import('@/views/system/user/index.vue'),
  meta: { 
    title: '用户管理', 
    icon: 'UserOutlined', 
    permission: 'system:user',
    cache: true,        // 是否缓存页面
    hidden: false,      // 是否隐藏菜单
    order: 1,           // 菜单排序（数字越大越靠前）
  },
}
```

**Meta 字段说明**：
| 字段 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `title` | 页面标题/菜单名称 | string | - |
| `icon` | 菜单图标 | string | - |
| `permission` | 权限标识 | string | - |
| `cache` | 是否缓存页面 | boolean | true |
| `hidden` | 是否隐藏菜单 | boolean | false |
| `order` | 菜单排序 | number | - |

### Step 3: 创建 API 接口

**位置**: `src/api/modules/模块名.ts`

```typescript
import request from '@/utils/request'

export interface UserParams {
  page: number
  pageSize: number
  username?: string
}

export interface UserItem {
  id: number
  username: string
  status: number
  createTime: string
}

export const userApi = {
  getList(params: UserParams) {
    return request.get<{ list: UserItem[], total: number }>('/api/users', { params })
  },
  create(data: Partial<UserItem>) {
    return request.post('/api/users', data)
  },
  update(id: number, data: Partial<UserItem>) {
    return request.put(`/api/users/${id}`, data)
  },
  delete(id: number) {
    return request.delete(`/api/users/${id}`)
  },
}
```

### Step 4: 配置按钮权限

**权限格式**: `模块:功能:操作`

```vue
<!-- 新增按钮 -->
<a-button v-permission="'system:user:add'">新增</a-button>

<!-- 编辑按钮 -->
<a-button v-permission="'system:user:edit'" type="link">编辑</a-button>

<!-- 删除按钮（必须二次确认） -->
<a-popconfirm title="确定删除？" @confirm="handleDelete">
  <a-button v-permission="'system:user:delete'" type="link" danger>删除</a-button>
</a-popconfirm>
```

---

## 🔐 权限系统

### 权限标识规范

**格式**: `模块:功能:操作`

**示例**：
- `system:user:view` - 查看用户列表
- `system:user:add` - 新增用户
- `system:user:edit` - 编辑用户
- `system:user:delete` - 删除用户
- `system:user:export` - 导出数据
- `*:*:*` - 超级管理员（所有权限）

### 代码中判断权限

```typescript
import { useUserStore } from '@/stores/modules/user'

const userStore = useUserStore()

// 简单判断
const hasPermission = (permission: string) => {
  return userStore.permissions.includes(permission) || 
         userStore.permissions.includes('*:*:*')
}

// 或使用 Composable（推荐）
import { usePermission } from '@/composables/usePermission'
const { hasPermission, hasAnyPermission } = usePermission()
```

详细用法查看 → [references/composables.md](references/composables.md)

---

## 📝 必须遵守的开发规范

### 代码规范
1. ✅ 必须使用 `<script setup lang="ts">`
2. ✅ 所有 API 必须有 TypeScript 类型定义
3. ✅ 所有按钮权限必须配置 `v-permission`
4. ✅ 删除操作必须有二次确认（`a-popconfirm` 或 `Modal.confirm`）

### 表格规范
1. ✅ 必须包含 `row-key`、`loading`、`pagination`
2. ✅ 操作列固定在右侧 - `fixed: 'right'`
3. ✅ 列数 > 5 时设置横向滚动 - `:scroll="{ x: 1200 }"`
4. ✅ 行 hover 必须变色

### 表单规范
1. ✅ 所有输入框必须有 `placeholder`
2. ✅ 必填项必须有验证规则
3. ✅ 提交按钮必须有 loading 状态
4. ✅ 弹窗表单宽度不超过 600px

### 视觉规范
1. ✅ 按钮必须有 hover 效果（颜色、阴影、位移动画）
2. ✅ 卡片必须有圆角和阴影（8px + `0 2px 8px`）
3. ✅ 间距使用统一系统（4px 倍数）
4. ✅ 文字颜色遵循层级（#1f1f1f → #595959 → #8c8c8c）

### 交互规范
1. ✅ 所有异步操作必须有 loading
2. ✅ 成功/失败必须有 message 提示
3. ✅ 删除操作必须二次确认
4. ✅ 表单验证失败必须滚动到错误位置

---

## 📁 项目结构

```
src/
├── api/modules/           # API 接口（按模块分类）
├── assets/styles/         # 全局样式
├── composables/           # 组合式函数（useLoading, usePermission, useTable）
├── config/                # 配置文件
├── directives/            # 自定义指令（v-permission）
├── layouts/               # 页面布局
│   ├── MainLayout.vue
│   └── components/
├── router/                # 路由配置
├── stores/modules/        # Pinia 状态管理
├── utils/                 # 工具函数
└── views/                 # 页面视图（按模块分类）
    ├── login/
    ├── dashboard/
    └── system/
        ├── user/
        ├── role/
        └── menu/
```

---

## 🎨 UI/UX 设计规范速览

### 色彩系统
```scss
// 主色调（蓝紫渐变）
$primary-color: #667eea;
$primary-dark: #4c5ce6;

// 功能色
$success-color: #52c41a;
$warning-color: #faad14;
$error-color: #ff4d4f;
```

### 间距系统
```scss
$space-sm: 8px;      // 按钮间距
$space-base: 16px;   // 卡片间距
$space-xl: 24px;     // 页面内边距
```

### 阴影规范
```scss
$shadow-card: 0 2px 8px rgba(0, 0, 0, 0.06);
$shadow-card-hover: 0 4px 16px rgba(0, 0, 0, 0.1);
```

完整设计规范 → [references/design-system.md](references/design-system.md)

---

## 🔧 常用 Composables

### useLoading - 加载状态管理
```typescript
const { loading, withLoading } = useLoading()

const fetchData = async () => {
  await withLoading(async () => {
    const res = await api.getList()
  })
}
```

### usePermission - 权限检查
```typescript
const { hasPermission } = usePermission()

const canEdit = hasPermission('system:user:edit')
```

### useTable - 表格状态管理
```typescript
const { dataSource, loading, pagination, fetchData } = useTable(api.getList)
```

完整 Composables 文档 → [references/composables.md](references/composables.md)

---

## 💡 最佳实践

### 何时使用哪个模板？

| 场景 | 推荐模板 | 原因 |
|------|---------|------|
| 简单数据管理 | [标准列表页](references/templates/standard-list-page.md) | 代码简洁，易于理解 |
| 复杂业务管理 | [高级搜索表格](references/templates/advanced-table.md) | 支持批量操作、行选择 |
| 数据统计展示 | 自定义 Dashboard | 使用 a-statistic + 图表 |

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件夹 | kebab-case | `user-management/` |
| Vue 文件 | PascalCase | `UserList.vue` |
| 变量/函数 | camelCase | `getUserList` |
| 权限标识 | 模块:功能:操作 | `system:user:add` |

---

## 📚 进阶资源

### 推荐阅读顺序
1. 先用[标准开发流程](#-标准开发流程4步法)快速上手
2. 根据需要查看详细模板和 Composables
3. 参考完整设计规范优化视觉细节

### 设计资源
- **配色方案**：[Coolors](https://coolors.co/)、[ColorHunt](https://colorhunt.co/)
- **图标库**：[Ant Design Icons](https://ant.design/components/icon-cn/)
- **设计灵感**：[Dribbble](https://dribbble.com/)

---

**版本**: v3.0 (优化版)  
**框架**: Ant Design Vue 4.x + Vue 3 + TypeScript  
**更新**: 2026-04-13  
**设计理念**: 现代、简洁、专业、注重用户体验
