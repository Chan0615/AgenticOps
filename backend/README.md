# AgenticOps 后端

基于 FastAPI 的异步 RESTful API 服务。

## 技术栈

- **框架**: FastAPI 0.109+
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据库**: MySQL + aiomysql
- **缓存**: Redis
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)

## 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   ├── common/       # 通用模块
│   │   │   └── auth.py   # 认证相关
│   │   └── system/       # 系统管理模块
│   │       ├── users.py  # 用户管理
│   │       ├── roles.py  # 角色管理
│   │       └── menus.py  # 菜单管理
│   ├── core/             # 核心配置
│   │   ├── config.py     # 配置管理
│   │   └── security.py   # 安全工具
│   ├── crud/             # 数据库操作
│   │   └── system/       # 系统 CRUD
│   ├── db/               # 数据库配置
│   │   └── database.py   # 数据库连接
│   ├── models/           # 数据模型
│   │   └── models.py     # SQLAlchemy 模型
│   └── schemas/          # Pydantic 模型
│       ├── common/       # 通用 Schema
│       └── system/       # 系统 Schema
├── main.py               # 应用入口
└── requirements.txt      # 依赖列表
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境

创建 `.env` 文件：

```env
# 应用配置
APP_NAME=AgenticOps
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=agenticops

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT 配置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS 配置
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 3. 创建数据库

```sql
CREATE DATABASE agenticops CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --port 8000

# 生产模式
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 认证模块 (common)
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/refresh | 刷新令牌 |
| GET | /api/auth/me | 获取当前用户 |
| PUT | /api/auth/me | 更新当前用户 |
| POST | /api/auth/change-password | 修改密码 |

### 用户管理 (system)
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/users/ | 获取用户列表 |
| GET | /api/users/{id} | 获取指定用户 |
| POST | /api/users/ | 创建用户 |
| PUT | /api/users/{id} | 更新用户 |
| DELETE | /api/users/{id} | 删除用户 |

### 角色管理 (system)
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/roles/ | 获取角色列表 |
| GET | /api/roles/{id} | 获取指定角色 |
| POST | /api/roles/ | 创建角色 |
| PUT | /api/roles/{id} | 更新角色 |
| DELETE | /api/roles/{id} | 删除角色 |

### 菜单管理 (system)
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/menus/ | 获取菜单树 |
| GET | /api/menus/all | 获取所有菜单 |
| GET | /api/menus/{id} | 获取指定菜单 |
| POST | /api/menus/ | 创建菜单 |
| PUT | /api/menus/{id} | 更新菜单 |
| DELETE | /api/menus/{id} | 删除菜单 |

## 数据模型

### 用户 (sys_user)
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

## 开发指南

### 添加新模块

1. 创建路由：`app/api/模块名/xxx.py`
2. 创建 CRUD：`app/crud/模块名/xxx.py`
3. 创建 Schema：`app/schemas/模块名/xxx.py`
4. 在 `app/main.py` 中注册路由

### 代码规范

- 使用 Python type hints
- 遵循 PEP 8
- 所有异步函数使用 `async/await`
- 使用 Pydantic 进行数据验证

## 依赖列表

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
aiomysql==0.2.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
redis==5.0.1
```
