# AgenticOps 后端服务

基于 FastAPI 的异步 RESTful API 服务，提供智能运维平台后端能力。

## ✨ 核心特性

- 🔐 JWT 认证与权限管理
- 📚 RAG 知识库与向量检索
- 🖥️ 服务器管理（SSH + SaltStack 混合架构）
- ⏰ 定时任务调度（Celery + Redis）
- 📜 脚本管理与执行
- 📊 操作日志与审计
- ⚡ 全异步架构（FastAPI + SQLAlchemy + aiomysql）
- 🎯 模块化设计（api/crud/schemas/services 分层）

## 技术栈

- **框架**: FastAPI 0.109+
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据库**: MySQL + aiomysql
- **缓存**: Redis
- **任务队列**: Celery + Redis
- **定时调度**: Celery Beat + croniter
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt
- **WebSocket**: websockets
- **SSH 连接**: Paramiko
- **运维集成**: SaltStack API

## 📁 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由层
│   │   ├── agent/        # Agent 模块（RAG 对话）
│   │   ├── auth/         # 认证模块
│   │   ├── common/       # 通用模块
│   │   ├── ops/          # 运维管理模块 ⭐
│   │   │   ├── __init__.py
│   │   │   ├── servers.py    # 服务器管理
│   │   │   ├── scripts.py    # 脚本管理
│   │   │   ├── tasks.py      # 定时任务
│   │   │   └── logs.py       # 执行日志
│   │   └── system/       # 系统管理模块
│   ├── core/             # 核心配置
│   ├── crud/             # 数据库操作层
│   │   ├── ops/          # 运维 CRUD ⭐
│   │   │   ├── __init__.py
│   │   │   ├── server.py     # 服务器 CRUD
│   │   │   ├── script.py     # 脚本 CRUD
│   │   │   ├── task.py       # 任务 CRUD
│   │   │   └── log.py        # 日志 CRUD
│   │   └── system/       # 系统 CRUD
│   ├── db/               # 数据库配置
│   ├── models/           # SQLAlchemy 数据模型
│   │   ├── models.py     # 系统模型
│   │   ├── agent.py      # Agent 模型
│   │   ├── log.py        # 日志模型
│   │   └── ops.py        # 运维模型 ⭐
│   ├── rag/              # RAG 核心逻辑
│   ├── schemas/          # Pydantic 数据验证
│   │   ├── server/       # 服务器 Schema（Ops 模块）
│   │   ├── script/       # 脚本 Schema ⭐
│   │   ├── task/         # 任务 Schema ⭐
│   │   ├── log/          # 日志 Schema ⭐
│   │   └── system/       # 系统 Schema
│   ├── services/         # 业务逻辑层
│   │   ├── ssh_service.py    # SSH 服务
│   │   └── salt_service.py   # SaltStack 服务
│   ├── tasks/            # Celery 任务 ⭐
│   │   ├── __init__.py
│   │   ├── salt_tasks.py     # SaltStack 任务
│   │   ├── ssh_tasks.py      # SSH 任务
│   │   └── scheduler.py      # 定时调度器
│   └── main.py           # FastAPI 应用入口
├── celery_app.py         # Celery 配置 ⭐
├── uploads/              # 文件上传目录
├── vector_db/            # 向量数据库存储
├── config.yaml.example   # 配置文件示例
├── init_db.py            # 数据库初始化脚本
├── requirements.txt      # Python 依赖
└── main.py               # 启动入口
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境

复制并编辑配置文件：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml`：

```yaml
# MySQL 配置
mysql:
  default:
    host: 10.225.138.121
    port: 3306
    user: root
    password: "your_password"
    database: kefu_ai

# Redis 配置
redis:
  default:
    host: 10.225.138.125
    port: 6579
    password: "your_redis_password"
    db: 20

# JWT 配置
jwt:
  secret_key: "your-secret-key-change-in-production"
  algorithm: HS256
  access_token_expire_minutes: 30
  refresh_token_expire_days: 7

# Saltstack 多环境配置
saltstack:
  fuchunyun:
    url: http://10.66.108.97
    salt_name: saltapi
    salt_pass: "your_salt_password"
  aliyun:
    url: http://10.136.74.9
    salt_name: saltapi
    salt_pass: "your_salt_password"

# AI 模型配置
ai:
  openai:
    enabled: false
    api_key: "your_api_key"
    base_url: "https://api.openai.com/v1"
    model: "gpt-4o"
```

### 3. 创建数据库

```sql
CREATE DATABASE kefu_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库

```bash
# 初始化所有表（系统表 + Agent表 + 运维表）
# 注意：会删除所有旧数据并重新创建，回到项目最初状态
python init_db.py
```

### 5. 启动服务

```bash
# 开发模式 - FastAPI 服务
uvicorn app.main:app --reload --port 8000

# 生产模式
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 启动 Celery Worker（新终端窗口）
celery -A celery_app worker --loglevel=info --concurrency=4

# 启动 Celery Beat 定时调度（新终端窗口）
celery -A celery_app beat --loglevel=info

# 启动 WebSocket SSH 服务器（新终端窗口）
python -m app.api.server.websocket_handler
```

**说明**：
- FastAPI 服务运行在 `http://localhost:8000`（RESTful API）
- Celery Worker 处理异步任务（SSH/SaltStack 执行）
- Celery Beat 定时调度器（每分钟检查定时任务）
- WebSocket SSH 服务器运行在 `ws://localhost:8765`（Web SSH 终端）
- Web SSH 终端功能需要同时启动 FastAPI 和 WebSocket 服务

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 API 端点

### 认证模块 (/api/auth)
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/refresh | 刷新令牌 |
| GET | /api/auth/me | 获取当前用户 |
| PUT | /api/auth/me | 更新当前用户 |
| POST | /api/auth/change-password | 修改密码 |

### 用户管理 (/api/users)
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/users/ | 获取用户列表 |
| GET | /api/users/{id} | 获取指定用户 |
| POST | /api/users/ | 创建用户 |
| PUT | /api/users/{id} | 更新用户 |
| DELETE | /api/users/{id} | 删除用户 |

### 角色管理 (/api/roles)
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/roles/ | 获取角色列表 |
| GET | /api/roles/{id} | 获取指定角色 |
| POST | /api/roles/ | 创建角色 |
| PUT | /api/roles/{id} | 更新角色 |
| DELETE | /api/roles/{id} | 删除角色 |

### 菜单管理 (/api/menus)
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/menus/ | 获取菜单树 |
| GET | /api/menus/all | 获取所有菜单 |
| GET | /api/menus/{id} | 获取指定菜单 |
| POST | /api/menus/ | 创建菜单 |
| PUT | /api/menus/{id} | 更新菜单 |
| DELETE | /api/menus/{id} | 删除菜单 |

### RAG 知识库 (/api/knowledge)
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/knowledge/upload | 上传文档 |
| GET | /api/knowledge/list | 获取知识库列表 |
| DELETE | /api/knowledge/{id} | 删除文档 |

### Agent 对话 (/api/agent)
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/agent/chat | 发起对话 |
| GET | /api/agent/conversations | 获取对话历史 |

### 服务器管理 (/api/ops/servers) ⭐
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/ops/servers | 获取服务器列表 |
| GET | /api/ops/servers/{id} | 获取服务器详情 |
| POST | /api/ops/servers | 创建服务器 |
| PUT | /api/ops/servers/{id} | 更新服务器 |
| DELETE | /api/ops/servers/{id} | 删除服务器 |
| POST | /api/ops/servers/test-connection | 测试连接 |

### 脚本管理 (/api/ops/scripts) ⭐
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/ops/scripts | 获取脚本列表 |
| GET | /api/ops/scripts/{id} | 获取脚本详情 |
| POST | /api/ops/scripts | 创建脚本 |
| PUT | /api/ops/scripts/{id} | 更新脚本 |
| DELETE | /api/ops/scripts/{id} | 删除脚本 |
| POST | /api/ops/scripts/test | 测试执行脚本 |

### 定时任务 (/api/ops/tasks) ⭐
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/ops/tasks | 获取任务列表 |
| GET | /api/ops/tasks/{id} | 获取任务详情 |
| POST | /api/ops/tasks | 创建任务 |
| PUT | /api/ops/tasks/{id} | 更新任务 |
| DELETE | /api/ops/tasks/{id} | 删除任务 |
| POST | /api/ops/tasks/{id}/toggle | 切换启用状态 |
| POST | /api/ops/tasks/trigger | 手动触发执行 |

### 执行日志 (/api/ops/logs) ⭐
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/ops/logs/execution | 获取执行日志列表 |
| GET | /api/ops/logs/execution/{id} | 获取日志详情 |

### WebSocket SSH 终端 (ws://localhost:8765)
| 动作 | 描述 |
|------|------|
| connect | 建立 SSH 连接（需提供 hostname, port, username, password） |
| input | 发送命令输入到 SSH 终端 |
| resize | 调整终端窗口大小 |
| disconnect | 断开 SSH 连接 |

## 🗄️ 数据模型

### 系统表

#### 用户 (sys_user)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| username | string | 用户名（唯一） |
| email | string | 邮箱（唯一） |
| password_hash | string | 密码哈希 |
| full_name | string | 真实姓名 |
| avatar | string | 头像URL |
| status | bool | 状态 |
| is_superuser | bool | 超级管理员 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 角色 (sys_role)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| name | string | 角色名称 |
| code | string | 角色代码（唯一） |
| description | string | 描述 |
| status | bool | 状态 |
| sort_order | int | 排序 |

### 菜单 (sys_menu)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| name | string | 菜单名称 |
| code | string | 菜单代码（唯一） |
| path | string | 路由路径 |
| component | string | 组件路径 |
| icon | string | 图标 |
| parent_id | int | 父菜单ID |
| sort_order | int | 排序 |
| type | string | 类型（menu/directory/button） |
| status | bool | 状态 |

### 运维表 ⭐

#### 服务器 (ops_server)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| name | string | 服务器名称 |
| hostname | string | IP地址或域名 |
| port | int | SSH端口 |
| username | string | 登录用户名 |
| auth_type | string | 认证方式（password/key） |
| salt_minion_id | string | Salt Minion ID |
| environment | string | 环境（production/staging/testing） |
| tags | json | 标签列表 |
| status | string | 状态（online/offline/unknown） |

#### 脚本 (ops_script)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| name | string | 脚本名称 |
| content | text | 脚本内容 |
| script_type | string | 类型（shell/python） |
| parameters | json | 参数定义 |
| timeout | int | 超时时间（秒） |

#### 定时任务 (ops_scheduled_task)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| name | string | 任务名称 |
| script_id | int | 关联脚本ID |
| server_ids | json | 目标服务器ID列表 |
| cron_expression | string | Cron表达式 |
| task_type | string | 执行方式（salt/ssh） |
| enabled | bool | 是否启用 |
| last_run_at | datetime | 上次执行时间 |
| next_run_at | datetime | 下次执行时间 |

#### 执行日志 (ops_task_execution_log)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | int | 主键 |
| task_id | int | 任务ID |
| server_id | int | 服务器ID |
| status | string | 状态（pending/running/success/failed） |
| command | text | 执行的命令 |
| output | text | 标准输出 |
| error | text | 错误输出 |
| exit_code | int | 退出码 |
| duration | float | 执行时长（秒） |

## 🏗️ 架构设计

### 混合架构：SSH + SaltStack

```
┌─────────────────────────────────────────┐
│          AgenticOps 平台                 │
├─────────────────┬───────────────────────┤
│  交互式终端操作   │    定时任务/批量操作    │
│   (实时敲命令)    │   (Cron/计划任务)      │
├─────────────────┼───────────────────────┤
│   Paramiko SSH  │    SaltStack + Celery  │
│  (WebSocket终端) │  (异步任务队列调度)     │
└─────────────────┴───────────────────────┘
```

**使用场景**：
- **Paramiko SSH**: Web 终端实时交互、单台服务器操作、调试排查
- **SaltStack**: 批量服务器操作、定时任务执行、统一配置管理

### 分层架构

```
请求流程：
API 路由 (api/) 
  ↓
业务逻辑 (services/)
  ↓
数据操作 (crud/)
  ↓
数据模型 (models/)
  ↓
数据库 (MySQL/Redis)
```

### 任务执行流程

```
用户创建定时任务
    ↓
保存到数据库 (enabled=True)
    ↓
Celery Beat 每分钟扫描
    ↓
匹配 Cron 表达式
    ↓
触发 Celery Worker
    ↓
选择执行方式 (Salt/SSH)
    ↓
执行命令并收集结果
    ↓
保存执行日志
    ↓
更新任务状态
```

### 配置管理

- 使用 YAML 配置文件 (`config.yaml`)
- 支持多环境配置（MySQL/Redis/Saltstack）
- 配置加载器：`app/core/config.py`

## 🚀 Celery 任务队列

### 启动命令

```bash
# Worker - 处理异步任务
celery -A celery_app worker --loglevel=info --concurrency=4

# Beat - 定时任务调度
celery -A celery_app beat --loglevel=info
```

### 任务队列

- **salt**: SaltStack 批量执行任务
- **ssh**: SSH 单台执行任务
- **scheduler**: 定时调度器任务

### 配置

Celery 配置从 `config.yaml` 的 Redis 配置自动读取，无需额外配置。

## 👨‍💻 开发指南

### 添加新模块

1. **创建路由**：`app/api/模块名/xxx.py`
2. **创建 CRUD**：`app/crud/模块名/xxx.py`
3. **创建 Schema**：`app/schemas/模块名/xxx.py`
4. **业务逻辑**（可选）：`app/services/xxx.py`
5. **注册路由**：在 `app/main.py` 中添加路由

### 代码规范

- 使用 Python type hints
- 遵循 PEP 8 规范
- 所有异步函数使用 `async/await`
- 使用 Pydantic 进行数据验证
- 错误处理使用 HTTPException

## 依赖列表

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.25
aiomysql>=0.2.0
python-jose[cryptography]>=3.3.0
bcrypt>=4.0.1
python-multipart>=0.0.6
pydantic>=2.5.3
redis>=5.0.1
celery[redis]>=5.3.0
croniter>=2.0.0
paramiko>=3.4.0
salt>=3006.0
websockets>=12.0
aiohttp>=3.9.0
```
