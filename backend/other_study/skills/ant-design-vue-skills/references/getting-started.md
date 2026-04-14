# 快速开始

## 项目初始化

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

**.env.development**:
```env
VITE_APP_ENV=development
VITE_APP_TITLE=企业管理系统
VITE_APP_BASE_API=http://tempapi.ops.com/api
VITE_PROJECT_CODE=flask_api_template
```

**.env.production**:
```env
VITE_APP_ENV=production
VITE_APP_TITLE=企业管理系统
VITE_APP_BASE_API=/api
VITE_PROJECT_CODE=flask_api_template
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

---

## 项目结构

```
src/
├── api/modules/           # API 接口层
├── assets/styles/         # 静态资源
├── config/                # 配置文件
├── directives/            # 自定义指令
├── layouts/               # 页面布局
├── router/                # 路由配置
├── stores/modules/        # Pinia 状态管理
├── utils/                 # 工具函数
└── views/                 # 页面视图
```

---

## 核心特性

### 1. LDAP 登录

- 账号密码登录
- 权限申请链接
- Token 自动管理

### 2. 按钮级权限

```vue
<a-button v-permission="'system:user:add'">新增</a-button>
```

### 3. 标准 CRUD

- 搜索表单
- 数据表格
- 新增/编辑弹窗
- 删除确认

---

## 开发流程

1. 创建页面文件
2. 添加路由配置
3. 创建 API 接口
4. 配置按钮权限

详见 [SKILL.md](../SKILL.md)
