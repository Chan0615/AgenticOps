# AgenticOps 智能平台

基于 uv + FastAPI + Vue3 + MySQL + Redis + AI 的智能管理平台。

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: MySQL
- **缓存**: Redis
- **认证**: JWT
- **ORM**: SQLAlchemy (异步)

### 前端
- **框架**: Vue 3
- **构建工具**: Vite
- **UI**: TailwindCSS
- **状态管理**: Pinia
- **HTTP**: Axios

### AI 集成
- 支持 AI 模型集成（扩展功能）

## 项目结构

```
AgenticOps/
├── backend/              # 后端项目
│   ├── app/
│   │   ├── api/        # API 路由
│   │   │   ├── common/ # 通用模块
│   │   │   └── system/ # 系统管理模块
│   │   ├── core/       # 核心配置
│   │   ├── crud/       # 数据库操作
│   │   ├── db/         # 数据库配置
│   │   ├── models/     # 数据模型
│   │   └── schemas/    # Pydantic 模型
│   └── requirements.txt
├── frontend/            # 前端项目
│   ├── src/
│   │   ├── api/        # API 接口
│   │   ├── layouts/    # 布局组件
│   │   ├── router/     # 路由配置
│   │   ├── stores/     # 状态管理
│   │   └── views/      # 页面组件
│   └── package.json
└── README.md           # 项目总览
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+

### 后端启动

```bash
# 安装依赖
cd backend

# 使用 uv 安装（会自动处理 Python 版本）
uv pip install -r requirements.txt

# 或者如果你想创建虚拟环境
uv venv
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库和 Redis

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 `http://localhost:5173` 即可看到登录页面。

## 数据库配置

编辑 `backend/.env` 文件：

```env
# MySQL 配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=agenticops

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

### 创建数据库

```sql
CREATE DATABASE agenticops CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 功能模块

### 已完成
- ✅ 用户登录/注册
- ✅ 用户管理
- ✅ 角色管理
- ✅ 菜单管理
- ✅ JWT 认证

### 开发中
- 🔄 AI 集成功能
- 🔄 权限控制优化
- 🔄 日志管理

## API 文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 部署

### Docker 部署（推荐）

```bash
# 构建并启动
docker-compose up -d
```

### 传统部署

1. 配置 Nginx 反向代理
2. 使用 Gunicorn 运行 FastAPI
3. 构建前端静态资源

## 开发指南

### 添加新模块

**后端**：
1. 在 `app/api/新建模块/` 创建路由文件
2. 在 `app/crud/新建模块/` 创建 CRUD 操作
3. 在 `app/schemas/新建模块/` 创建数据模型

**前端**：
1. 在 `src/api/新建模块/` 创建 API 接口
2. 在 `src/views/新建模块/` 创建页面组件
3. 在路由中注册新页面

### 代码规范

- 后端使用 Python type hints
- 前端使用 TypeScript
- 遵循 RESTful API 设计规范

## 许可证

MIT License
