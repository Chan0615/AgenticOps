# AgenticOps 前端

基于 Vue 3 的现代化管理后台前端。

## 技术栈

- **框架**: Vue 3.4+
- **构建工具**: Vite 5.0
- **路由**: Vue Router 4.2
- **状态管理**: Pinia 2.1
- **UI**: TailwindCSS 3.4
- **HTTP**: Axios 1.6
- **类型**: TypeScript 5.3
- **图标**: Lucide Vue Next

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口
│   │   ├── index.ts      # Axios 实例
│   │   └── system/       # 系统模块 API
│   │       ├── index.ts   # 导出
│   │       ├── types.ts   # 类型定义
│   │       ├── auth.ts    # 认证接口
│   │       ├── user.ts    # 用户接口
│   │       ├── role.ts    # 角色接口
│   │       └── menu.ts    # 菜单接口
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   ├── layouts/          # 布局组件
│   │   └── MainLayout.vue # 主布局
│   ├── router/           # 路由配置
│   │   └── index.ts      # 路由定义
│   ├── stores/           # Pinia 状态管理
│   │   └── auth.ts       # 认证状态
│   ├── style.css         # 全局样式
│   ├── views/            # 页面组件
│   │   ├── Login.vue     # 登录页面
│   │   ├── Dashboard.vue  # 仪表盘
│   │   ├── Settings.vue   # 设置容器
│   │   └── settings/      # 设置子页面
│   │       ├── UserManagement.vue
│   │       ├── RoleManagement.vue
│   │       └── MenuManagement.vue
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── index.html            # HTML 模板
├── package.json          # 依赖配置
├── tsconfig.json         # TypeScript 配置
├── vite.config.ts        # Vite 配置
├── tailwind.config.js    # TailwindCSS 配置
└── postcss.config.js     # PostCSS 配置
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

## 页面路由

| 路径 | 页面 | 描述 |
|------|------|------|
| /login | Login | 登录页面 |
| / | MainLayout | 主布局（需登录） |
| /dashboard | Dashboard | 仪表盘 |
| /settings/users | UserManagement | 用户管理 |
| /settings/roles | RoleManagement | 角色管理 |
| /settings/menus | MenuManagement | 菜单管理 |

## 登录页面

采用动画角色效果的现代化登录界面：
- 登录/注册 Tab 切换
- 动画人物角色
- 浮动装饰元素
- 密码显示/隐藏
- 表单验证
- 响应式设计

## API 接口

### 认证 (auth)

```typescript
// 登录
authApi.login({ username, password })

// 注册
authApi.register({ username, email, password })

// 获取当前用户
authApi.getMe()

// 更新个人信息
authApi.updateMe({ email, full_name })

// 修改密码
authApi.changePassword(oldPassword, newPassword)
```

### 用户管理 (user)

```typescript
// 获取用户列表
userApi.getUsers(skip, limit)

// 获取单个用户
userApi.getUser(id)

// 创建用户
userApi.createUser({ username, email, password })

// 更新用户
userApi.updateUser(id, { email, status })

// 删除用户
userApi.deleteUser(id)
```

### 角色管理 (role)

```typescript
// 获取角色列表
roleApi.getRoles(skip, limit)

// 获取单个角色
roleApi.getRole(id)

// 创建角色
roleApi.createRole({ name, code, description, menu_ids })

// 更新角色
roleApi.updateRole(id, { name, status, menu_ids })

// 删除角色
roleApi.deleteRole(id)
```

### 菜单管理 (menu)

```typescript
// 获取菜单树
menuApi.getMenus()

// 获取扁平菜单列表
menuApi.getAllMenus(skip, limit)

// 获取单个菜单
menuApi.getMenu(id)

// 创建菜单
menuApi.createMenu({ name, code, path, component, parent_id })

// 更新菜单
menuApi.updateMenu(id, { name, status })

// 删除菜单
menuApi.deleteMenu(id)
```

## 状态管理

### Auth Store

```typescript
const authStore = useAuthStore()

// 属性
authStore.user       // 当前用户
authStore.token      // JWT 令牌
authStore.isAuthenticated  // 是否已登录
authStore.isSuperuser      // 是否超级管理员

// 方法
authStore.login(credentials)    // 登录
authStore.register(data)        // 注册
authStore.logout()              // 登出
authStore.fetchUser()           // 获取用户信息
authStore.updateProfile(data)   // 更新资料
```

## 开发指南

### 添加新页面

1. 在 `src/views/` 创建页面组件
2. 在 `src/router/index.ts` 添加路由
3. 在侧边栏添加导航链接

### 添加新 API

1. 在 `src/api/system/` 创建 API 文件
2. 定义类型和接口
3. 在 `src/api/system/index.ts` 导出

### 使用 TailwindCSS

组件类名遵循 TailwindCSS 规范：

```vue
<div class="p-4 bg-white rounded-lg shadow-sm">
  <h1 class="text-xl font-bold text-gray-800">标题</h1>
</div>
```

## 依赖列表

### 生产依赖
```json
{
  "vue": "^3.4.15",
  "vue-router": "^4.2.5",
  "pinia": "^2.1.7",
  "axios": "^1.6.5",
  "@vueuse/core": "^10.7.2",
  "lucide-vue-next": "^0.312.0",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.1.0",
  "tailwind-merge": "^2.2.0",
  "recharts": "^2.12.0"
}
```

### 开发依赖
```json
{
  "@vitejs/plugin-vue": "^5.0.3",
  "typescript": "^5.3.3",
  "vite": "^5.0.12",
  "vue-tsc": "^1.8.27",
  "autoprefixer": "^10.4.17",
  "postcss": "^8.4.33",
  "tailwindcss": "^3.4.1"
}
```

## 环境变量

```env
VITE_API_BASE_URL=/api
```

## 生产部署

```bash
# 构建
npm run build

# 构建产物在 dist/ 目录
# 可使用任意静态文件服务器部署
```
