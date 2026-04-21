# AgenticOps 智能运维平台

基于 FastAPI + Vue 3 的一体化智能运维平台，覆盖系统权限、RAG 知识库、运维资产管理、脚本分发、定时任务与执行日志，并内置**运维 AI 助手**——通过自然语言对话即可完成所有运维操作，同时支持通过 MCP 协议与 Claude Desktop 等 AI 工具直接集成。

## 技术栈

### 后端
- FastAPI、Uvicorn
- SQLAlchemy 2.x（异步）+ MySQL（aiomysql）
- Redis + Celery（worker/beat）
- JWT（python-jose）认证
- YAML 配置中心（`backend/config.yaml`）
- AI 集成：OpenAI 兼容接口（支持 DeepSeek / 阿里云 Qwen / OpenAI）、Function Calling、SSE 流式输出
- RAG 相关：LangChain、FAISS、Sentence Transformers
- 运维集成：SaltStack API（多环境）、JumpServer API（连接验证与运维流程）
- MCP：Model Context Protocol（供 Claude Desktop / Cursor 等工具直接调用）

### 前端
- Vue 3 + TypeScript + Vite
- Ant Design Vue 4.x
- Pinia + Vue Router + Axios
- TailwindCSS（辅助样式）
- marked.js（Markdown 渲染）

## 已开发功能

### 系统管理
- 用户管理：用户 CRUD、状态控制
- 角色管理：角色权限绑定
- 菜单管理：菜单树、按钮权限、图标配置
- 登录/鉴权：JWT 登录与会话态管理

### 运维模块（`/api/ops/*`）
- 服务器管理：资产维护、连接测试（JumpServer / SaltStack）
- 脚本管理：脚本上传、编辑、通过 Salt 分发到目标服务器
- 脚本版本管理：版本号自动递增、历史查看、版本对比（unified diff）、一键回滚
- 定时任务：Cron 调度（Celery Beat）、启停、手动触发
- 自然语言转 Cron：中文描述自动转换为标准 Cron 表达式
- 执行日志：任务执行记录与结果查看
- 运维看板：真实数据概览、近 7 天趋势图、系统公告管理
- 项目与分组：脚本/任务按项目维度组织管理

### 运维 AI 助手（`/api/ops/ai/*`）

通过自然语言对话完成所有运维操作，与页面功能等价。

**只读操作（AI 自主执行）**
- 查询服务器列表（支持环境、状态过滤）
- 搜索脚本库
- 查询定时任务（启用/禁用状态筛选）
- 查询执行日志（任务名、服务器、状态过滤）
- 解析 Cron 表达式含义
- 自然语言转 Cron 表达式

**写操作（AI 生成方案，用户确认后执行）**
- 在指定服务器上执行 Shell 命令/脚本
- 创建新的定时任务
- 启用/禁用定时任务

**交互特性**
- 支持 SSE 流式输出（逐字显示 AI 回复）
- 多轮对话历史持久化
- 写操作确认弹窗，防止误操作
- 快捷提示入口，降低上手成本

### 知识库与 RAG 助手
- RAG 知识库管理（文档上传、分块、检索）
- AI 问答（基于知识库内容）与通用系统助手

### MCP Server（`backend/mcp_server.py`）

将运维工具能力以 Model Context Protocol 对外暴露，供 Claude Desktop、Cursor 等工具直接调用。

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "agenticops": {
      "command": "python",
      "args": ["D:\\path\\to\\AgenticOps\\backend\\mcp_server.py"],
      "env": {
        "CONFIG_FILE": "D:\\path\\to\\AgenticOps\\backend\\config.yaml"
      }
    }
  }
}
```

安装依赖：`pip install mcp`

## 项目结构

```text
AgenticOps/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ auth/          # 登录、Token 刷新
│  │  │  ├─ system/        # 用户、角色、菜单
│  │  │  ├─ agent/         # RAG 知识库 & 问答
│  │  │  ├─ common/        # 操作日志
│  │  │  └─ ops/           # 运维核心 + AI 助手
│  │  │     ├─ servers.py
│  │  │     ├─ scripts.py
│  │  │     ├─ tasks.py
│  │  │     ├─ logs.py
│  │  │     ├─ dashboard.py
│  │  │     └─ ai_chat.py  # 运维 AI 助手路由
│  │  ├─ core/
│  │  │  ├─ ai.py          # 公共 LLM 调用层（Function Calling）
│  │  │  ├─ config.py
│  │  │  └─ security.py
│  │  ├─ crud/             # 数据访问层
│  │  ├─ models/           # ORM 模型
│  │  ├─ rag/
│  │  │  └─ tools.py       # 工具集（基础工具 + 运维工具）
│  │  ├─ schemas/
│  │  │  └─ ops_agent.py   # AI 助手请求/响应 Schema
│  │  └─ services/
│  │     ├─ ops_agent.py   # 运维 AI 对话核心服务
│  │     ├─ rag_agent.py   # RAG 知识库对话服务
│  │     ├─ salt_service.py
│  │     └─ jumpserver_service.py
│  ├─ mcp_server.py        # MCP stdio 服务器
│  ├─ config.yaml.example
│  ├─ init_db.py
│  └─ requirements.txt
└─ frontend/
   └─ src/
      ├─ api/ops/
      │  └─ ai.ts           # 运维 AI API 客户端（含 SSE）
      ├─ views/ops/
      │  └─ OpsAssistant.vue # 运维 AI 助手页面
      └─ router/index.ts
```

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- MySQL 8+
- Redis 6+

### 1) 后端启动

```bash
cd backend

# 首次：复制配置文件并填写数据库/AI 配置
cp config.yaml.example config.yaml

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（注意：该脚本默认会重建表，请先确认环境）
python init_db.py

# 启动 API（推荐限制热重载目录，避免上传脚本触发重启）
uvicorn app.main:app --reload --reload-dir app --port 8000

# 新终端：启动 Celery Worker（定时任务执行）
celery -A celery_app worker --loglevel=info -Q salt,scheduler

# 新终端：启动 Celery Beat（定时任务调度）
celery -A celery_app beat --loglevel=info
```

### 2) 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问：`http://localhost:5173`，默认账号：`admin / admin123`

### 3) 配置 AI 功能

编辑 `backend/config.yaml`，填写 AI 服务配置（三选一）：

```yaml
ai:
  qwen:                         # 阿里云 DashScope（推荐）
    enabled: true
    api_key: "sk-xxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model: "qwen-max"

  deepseek:                     # DeepSeek
    enabled: false
    api_key: "sk-xxx"
    base_url: "https://api.deepseek.com/v1"
    model: "deepseek-chat"

  openai:                       # OpenAI
    enabled: false
    api_key: "sk-xxx"
    base_url: "https://api.openai.com/v1"
    model: "gpt-4o"
```

### 4) 启用运维 AI 助手菜单

在「菜单管理」页面添加一条菜单记录：

| 字段 | 值 |
|------|-----|
| 名称 | 运维助手 |
| 路径 | `/ops/assistant` |
| 图标 | `RobotOutlined` |
| 上级菜单 | 运维管理 |

## AI 助手使用示例

```
用户：查看所有生产环境的服务器

AI：共找到 12 台服务器（显示前 12 台）：
- ID:1 | web-prod-01 | 192.168.1.10 | 环境:production | 状态:online
- ID:2 | web-prod-02 | 192.168.1.11 | 环境:production | 状态:online
...

用户：最近有没有执行失败的任务？

AI：共找到 3 条失败记录：
- ❌ [01-15 03:00] 数据库备份 @ db-prod-01(192.168.2.1) | 耗时:- | 退出码:1
...

用户：帮我在 web-prod-01 上执行 systemctl restart nginx

AI：我需要执行一个操作，请确认后继续：
    在 1 台服务器上执行命令：
    $ systemctl restart nginx
    目标服务器 ID：[1]

    [确认执行]  [取消]

用户：（点击确认）

AI：✅ 操作已执行：
    ✅ web-prod-01(192.168.1.10): 成功
```

## 关键说明

- 后端入口：`backend/app/main.py`，命令：`uvicorn app.main:app --reload --port 8000`
- `backend/config.yaml` 为本地配置，已 gitignore，请勿提交敏感信息
- `python init_db.py` 默认会**销毁重建**所有表，请谨慎在生产环境执行
- 旧版 `/server/*` 路由已迁移至 `/ops/*`；旧 SSH WebSocket 直连已下线

## API 路由一览

### 认证
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 登录 |
| POST | `/api/auth/refresh` | 刷新 Token |
| GET  | `/api/auth/me` | 当前用户信息 |

### 运维 AI 助手
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ops/ai/chat` | 对话（非流式） |
| POST | `/api/ops/ai/chat/stream` | 对话（SSE 流式） |
| POST | `/api/ops/ai/confirm` | 确认执行写操作 |
| GET  | `/api/ops/ai/conversations` | 对话列表 |
| GET  | `/api/ops/ai/conversations/{id}` | 对话详情 |
| DELETE | `/api/ops/ai/conversations/{id}` | 删除对话 |

### 运维模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/ops/servers` | 服务器列表/创建 |
| POST | `/api/ops/servers/test-connection` | 测试连通性 |
| GET/POST | `/api/ops/scripts` | 脚本列表/上传 |
| GET | `/api/ops/scripts/{id}/versions` | 版本列表 |
| GET | `/api/ops/scripts/{id}/versions/compare` | 版本对比 |
| POST | `/api/ops/scripts/{id}/rollback` | 版本回滚 |
| POST | `/api/ops/scripts/{id}/distribute` | 分发到服务器 |
| GET/POST | `/api/ops/tasks` | 定时任务列表/创建 |
| POST | `/api/ops/tasks/{id}/toggle` | 启用/禁用任务 |
| POST | `/api/ops/tasks/trigger` | 手动触发任务 |
| POST | `/api/ops/tasks/cron/natural` | 自然语言转 Cron |
| GET  | `/api/ops/logs/execution` | 执行日志列表 |
| GET  | `/api/ops/dashboard/overview` | 看板概览 |

### 知识库（RAG）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/rag/knowledge-bases` | 知识库管理 |
| POST | `/api/rag/knowledge-bases/{id}/documents` | 上传文档 |
| POST | `/api/rag/chat` | AI 问答（非流式） |
| POST | `/api/rag/chat/stream` | AI 问答（SSE 流式） |

完整文档：后端启动后访问 `http://localhost:8000/docs`

## 可用脚本

### 前端
```bash
npm run dev        # 开发模式
npm run build      # 生产构建
npm run typecheck  # TypeScript 类型检查
```

### 后端
```bash
python init_db.py               # 初始化/重建数据库（⚠️ 破坏性）
python add_server_menu.py       # 旧菜单 /server/* → /ops/* 迁移
python mcp_server.py            # 启动 MCP Server（需 pip install mcp）
```

## 下一步规划

- 凭据中心（主机凭据加密、轮换、权限隔离）
- 运维审批流（高风险任务强制审批，替代当前前端确认框）
- 告警中心（阈值触发、通知渠道、告警收敛）
- 任务批量编排（分批执行、并发控制、失败回滚）
- 主机自动发现与 CMDB 同步
- AI 助手多工具并行调用（当前每次处理一个工具调用）
- 向量化检索升级（FAISS/Milvus 替代当前 MySQL LIKE 检索）

## License

MIT
