# CHAN AgenticOps 智能管理平台

基于 FastAPI + Vue3 + MySQL + Redis 的智能管理平台，支持 RAG 知识库问答、服务器运维管理、Web SSH 终端等功能。

## ✨ 核心特性

- 🔐 **完整的权限系统**：用户、角色、菜单三级权限管理
- 🤖 **RAG 知识库**：基于向量数据库的智能问答系统
- 📚 **文档管理**：支持 PDF 等文档上传与向量化处理
- 🖥️ **服务器管理**：SaltStack 批量管理 + Paramiko SSH 单台管理
- 🔧 **Web SSH 终端**：浏览器中直接远程连接服务器
- 💬 **自然语言运维**：AI 驱动的智能命令执行
- 🎨 **现代化界面**：Arco Design Pro 风格，流畅的交互体验
- ⚡ **高性能架构**：异步 FastAPI + SQLAlchemy + Redis 缓存

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI 0.109+
- **数据库**: MySQL 8.0+ (aiomysql 异步驱动)
- **缓存**: Redis 6.0+
- **ORM**: SQLAlchemy 2.0 (异步)
- **认证**: JWT (python-jose)
- **向量数据库**: FAISS
- **运维集成**: Saltstack API
- **配置管理**: YAML 配置文件

### 前端
- **框架**: Vue 3.4+ (Composition API)
- **UI 库**: Arco Design Vue
- **构建工具**: Vite 5.0
- **路由**: Vue Router 4.2
- **状态管理**: Pinia 2.1
- **样式**: TailwindCSS 3.4
- **HTTP 客户端**: Axios 1.6
- **类型系统**: TypeScript 5.3
- **终端组件**: xterm.js (Web SSH)

### AI & RAG
- **向量检索**: FAISS
- **文档解析**: LangChain
- **模型集成**: 支持 OpenAI、DeepSeek 等多模型
- **智能对话**: 基于知识库的 RAG 问答

### 服务器管理
- **批量管理**: SaltStack API 集成（支持多环境）
- **SSH 连接**: Paramiko 实现单台服务器管理
- **Web 终端**: WebSocket + xterm.js 实现交互式终端
- **自然语言**: AI 驱动的命令生成与执行

## 📁 项目结构

```
AgenticOps/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由层
│   │   │   ├── agent/         # Agent 模块（RAG 对话）
│   │   │   ├── auth/          # 认证模块
│   │   │   ├── server/        # 服务器管理（SaltStack + SSH）
│   │   │   └── system/        # 系统管理（用户、角色、菜单）
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # YAML 配置加载器
│   │   │   └── security.py    # 安全工具（JWT、密码）
│   │   ├── crud/              # 数据库操作层
│   │   │   ├── agent/         # Agent 相关 CRUD
│   │   │   └── system/        # 系统管理 CRUD
│   │   ├── db/                # 数据库连接
│   │   ├── models/            # SQLAlchemy 数据模型
│   │   │   ├── models.py      # 系统管理模型
│   │   │   ├── agent.py       # Agent RAG 模型
│   │   │   └── server.py      # 服务器管理模型
│   │   ├── rag/               # RAG 核心逻辑
│   │   ├── schemas/           # Pydantic 数据验证
│   │   └── services/          # 业务逻辑层
│   │       ├── rag_agent.py   # RAG Agent 服务
│   │       ├── salt_service.py# SaltStack 服务
│   │       └── ssh_service.py # SSH 连接服务
│   ├── uploads/               # 文件上传目录
│   ├── vector_db/             # 向量数据库存储
│   ├── config.yaml.example    # 配置文件示例
│   ├── init_db.py             # 数据库初始化脚本
│   └── requirements.txt       # Python 依赖
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── api/               # API 接口层
│   │   │   ├── agent/         # Agent 相关接口
│   │   │   ├── server/        # 服务器管理接口
│   │   │   └── system/        # 系统管理接口
│   │   ├── components/        # 公共组件
│   │   │   └── SSHTerminal.vue# Web SSH 终端组件
│   │   ├── layouts/           # 布局组件
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia 状态管理
│   │   └── views/             # 页面组件
│   │       ├── rag/           # RAG 对话界面
│   │       ├── server/        # 服务器管理
│   │       └── settings/      # 系统设置
│   └── package.json
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+

### 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp config.yaml.example config.yaml
# 编辑 config.yaml 配置数据库、Redis、Saltstack 等

# 4. 初始化数据库
python init_db.py

# 5. 启动 FastAPI 服务
uvicorn app.main:app --reload --port 8000

# 6. 启动 Celery Worker（新终端窗口）
# Windows 建议加 -P solo
celery -A celery_app worker --loglevel=info -Q salt,scheduler -P solo

# 7. 启动 Celery Beat（新终端窗口）
celery -A celery_app beat --loglevel=info
```

**说明**：
- FastAPI 服务运行在 `http://localhost:8000`
- 定时任务与手动触发依赖 Celery Worker + Beat
- 任务执行结果会写入 `ops_task_execution_log`

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 `http://localhost:5173` 即可看到登录页面。

## ⚙️ 配置说明

项目使用 `config.yaml` 进行配置，复制 `config.yaml.example` 为 `config.yaml` 后修改：

```yaml
# MySQL 数据库配置
mysql:
  default:
    host: "your_mysql_host"
    port: 3306
    user: root
    password: "your_password"
    database: "your_database_name"

# Redis 缓存配置
redis:
  default:
    host: "your_redis_host"
    port: 6579
    password: "your_redis_password"
    db: 20

# Saltstack 多环境配置
saltstack:
  fuchunyun:
    url: "your_salt_url"
    salt_name: "your_salt_name"
    salt_pass: "your_salt_password"
  aliyun:
    url: "your_salt_url"
    salt_name: "your_salt_name"
    salt_pass: "your_salt_password"
  # ... 更多环境

# AI 模型配置
ai:
  openai:
    enabled: false
    api_key: "your_api_key"
    base_url: "https://api.openai.com/v1"
    model: "gpt-4o"
  deepseek:
    enabled: false
    api_key: "your_api_key"
    base_url: "https://api.deepseek.com/v1"
    model: "deepseek-chat"
```

## 📦 功能模块

### ✅ 已完成

| 功能模块 | 说明 |
|----------|------|
| 认证系统 | 用户登录/注册、JWT 令牌、密码加密 |
| 用户管理 | 用户 CRUD、状态管理、角色分配 |
| 角色管理 | 角色权限、菜单关联、角色 CRUD |
| 菜单管理 | 动态菜单树、路由配置、权限控制 |
| RAG 知识库 | 文档上传、向量化存储、智能检索 |
| 智能对话 | 基于知识库的问答系统、对话历史 |
| 服务器管理 | SaltStack 批量管理 + SSH 单台管理 |
| Web SSH 终端 | 浏览器交互式终端（xterm.js） |
| 多环境支持 | SaltStack 多集群管理（富春云、阿里云、滨江等） |
| 界面优化 | 移除冗余标题，优化服务器列表展示（隐藏ID，描述悬浮展示，固定操作栏） |

### 🚧 开发中

| 功能模块 | 说明 |
|----------|------|
| 权限粒度优化 | 按钮级权限 |
| 操作日志审计 | 系统操作日志记录与审计 |
| 数据可视化仪表盘 | 系统监控数据可视化展示 |
| AI 自然语言运维 | 智能命令生成与执行 |
| 服务器监控告警 | 服务器状态监控与异常告警 |

## 📖 API 文档

启动后端服务后，访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要接口

#### 认证模块
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/refresh` - 刷新令牌
- `GET /api/auth/me` - 获取当前用户

#### 系统管理
- `GET/POST/PUT/DELETE /api/users/*` - 用户管理
- `GET/POST/PUT/DELETE /api/roles/*` - 角色管理
- `GET/POST/PUT/DELETE /api/menus/*` - 菜单管理

#### Agent & RAG
- `POST /api/rag/knowledge-bases` - 创建知识库
- `POST /api/rag/chat` - 智能对话
- `POST /api/rag/chat/stream` - 流式对话
- `GET /api/rag/conversations` - 对话列表

#### 服务器管理
- `POST /api/server/salt/{env}/execute` - 执行 Salt 命令
- `GET /api/server/salt/{env}/minions` - 获取 Minion 列表
- `POST /api/server/salt/{env}/ping` - 测试 Minion 连接
- `POST /api/server/salt/{env}/command` - 执行 Shell 命令
- `POST /api/server/ssh/execute` - SSH 执行命令
- `WebSocket ws://localhost:8765` - SSH 终端连接

## 🛡️ 部署

### Docker 部署（推荐）

```bash
# 构建并启动
docker-compose up -d
```

### 生产环境部署

1. **后端部署**
   ```bash
   # 使用 Gunicorn 运行
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

2. **前端部署**
   ```bash
   cd frontend
   npm run build
   # 将 dist/ 目录部署到 Nginx
   ```

3. **Nginx 配置**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
       }
       
       location / {
           root /path/to/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
   }
   ```

## 👨‍💻 开发指南

### 添加新模块

**后端**：
1. 在 `app/api/模块名/` 创建路由文件
2. 在 `app/crud/模块名/` 创建 CRUD 操作
3. 在 `app/schemas/模块名/` 创建数据模型
4. 在 `app/services/` 添加业务逻辑（可选）
5. 在 `app/main.py` 中注册路由

**前端**：
1. 在 `src/api/模块名/` 创建 API 接口
2. 在 `src/views/模块名/` 创建页面组件
3. 在 `src/router/index.ts` 中注册路由
4. 在主布局中添加导航菜单

### 代码规范

- **后端**：
  - 使用 Python type hints
  - 遵循 PEP 8 规范
  - 异步函数使用 `async/await`
  - 使用 Pydantic 进行数据验证
  
- **前端**：
  - 使用 TypeScript 类型系统
  - 遵循 Vue 3 Composition API 最佳实践
  - 组件使用 `<script setup>` 语法
  - 样式使用 TailwindCSS 原子类

### Git 工作流

```bash
# 功能分支开发
git checkout -b feature/your-feature

# 提交代码
git add .
git commit -m "feat: 添加 xxx 功能"

# 推送分支
git push origin feature/your-feature
```

## 许可证

MIT License
