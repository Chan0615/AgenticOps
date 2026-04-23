# AgenticOps 智能运维平台

基于 FastAPI + Vue 3 的一体化智能运维平台，集成 **AI 系统助手**、**RAG 知识库**、**智能问数（NL2SQL）**、运维资产管理等核心能力。

## 功能模块

### 系统管理
- 用户 / 角色 / 菜单管理，按钮级权限控制
- JWT 认证（access + refresh token）
- 操作日志审计

### AI 系统助手（`/assistant`）
- 基于 Function Calling 的运维 AI 对话
- 只读工具（查询服务器、脚本、任务、日志）自动执行
- 写操作（执行命令、创建/启停任务）需用户确认
- SSE 流式输出，多轮对话持久化

### RAG 知识库（`/rag/*`）
- 知识库管理：创建 / 编辑 / 删除
- 文档上传：支持 PDF、Word、Markdown、TXT
- LLM 语义分割：大模型识别最佳切分位置
- 向量存储：PostgreSQL + pgvector
- 双重召回检索：向量相似度搜索 + BM25 关键词检索
- 加权融合排序：向量 70% + BM25 30%
- 对话记忆：ConversationBufferMemory（最近 16 条）

### 智能问数（`/dataquery/*`）
- 数据源管理：多数据库连接（MySQL / PostgreSQL），元数据同步
- NL2SQL：自然语言 → SQL，AI 生成查询并执行
- 结果展示：表格 + 图表（柱状图/折线图/饼图）+ AI 摘要
- SQL 安全校验：仅允许 SELECT，自动限制行数
- Excel 导出：大数据量结果导出为 .xlsx

### 运维管理（`/ops/*`）
- 服务器资产管理，连接测试（JumpServer / SaltStack）
- 脚本管理：上传、版本管理、分发执行
- 定时任务：Cron 调度（Celery Beat），自然语言转 Cron
- 执行日志：完整的任务执行记录
- 运维看板：数据概览 + 趋势图

### MCP Server
- 通过 Model Context Protocol 对外暴露运维工具
- 支持 Claude Desktop、Cursor 等 AI 工具直接调用

## 技术栈

| 层 | 技术 |
|----|------|
| 后端框架 | FastAPI + Uvicorn（异步） |
| 主数据库 | MySQL 8+ via aiomysql + SQLAlchemy 2.0 |
| 向量数据库 | PostgreSQL 16 + pgvector（RAG 语义检索） |
| 缓存/队列 | Redis + Celery（worker/beat） |
| AI 集成 | OpenAI 兼容 API（Qwen / DeepSeek / OpenAI）、Function Calling、Embedding API |
| 前端框架 | Vue 3 + TypeScript + Vite |
| UI 组件 | Ant Design Vue 4.x |
| 状态管理 | Pinia + Vue Router |
| 样式 | TailwindCSS |
| 图表 | ECharts |
| Markdown | marked.js |

## 项目结构

```
AgenticOps/
├── backend/
│   ├── app/
│   │   ├── api/                  # API 路由
│   │   │   ├── auth/             # 认证
│   │   │   ├── system/           # 用户/角色/菜单
│   │   │   ├── agent/            # RAG 知识库 + 系统助手
│   │   │   ├── ops/              # 运维管理
│   │   │   ├── dataquery/        # 智能问数
│   │   │   └── common/           # 操作日志
│   │   ├── core/                 # 配置/安全/AI调用层
│   │   ├── crud/                 # 数据访问层
│   │   ├── db/                   # 数据库连接（MySQL + pgvector）
│   │   ├── models/               # ORM 模型
│   │   ├── schemas/              # Pydantic Schema
│   │   ├── services/             # 业务服务层
│   │   │   ├── rag_agent.py      # RAG 对话服务
│   │   │   ├── system_agent.py   # 系统 AI 助手
│   │   │   ├── dataquery_service.py  # NL2SQL 服务
│   │   │   ├── vector_store.py   # 向量存储 + Embedding
│   │   │   ├── document_processor.py # 文档解析 + 语义分割
│   │   │   ├── hybrid_retriever.py   # 混合检索
│   │   │   └── db_connector.py   # 多数据源连接管理
│   │   └── rag/                  # RAG 工具集
│   ├── config.yaml.example       # 配置模板
│   ├── init_db.py                # 数据库初始化（破坏性）
│   ├── init_pgvector.py          # pgvector 表初始化
│   ├── add_dataquery_menu.py     # 智能问数菜单迁移
│   ├── add_server_menu.py        # 运维菜单迁移
│   ├── mcp_server.py             # MCP Server
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/                  # API 客户端
│       ├── views/                # 页面组件
│       │   ├── rag/              # RAG 知识库 + 对话
│       │   ├── dataquery/        # 智能问数
│       │   ├── assistant/        # AI 系统助手
│       │   ├── ops/              # 运维管理
│       │   └── settings/         # 系统设置
│       ├── layouts/              # 布局组件
│       └── router/               # 路由配置
├── DEPLOY_MANUAL.md              # 手动部署指南
├── DEPLOY_DOCKER.md              # Docker 部署指南
├── PGVECTOR_INSTALL.md           # pgvector 安装指南
└── STARTUP_GUIDE.md              # 本地开发指南
```

## 快速开始

详见 [01-本地开发指南](docs/01-本地开发指南.md)。

### 最简步骤

```bash
# 后端
cd backend
cp config.yaml.example config.yaml   # 编辑填入实际配置
pip install -r requirements.txt
python init_db.py                     # 初始化数据库（⚠️ 破坏性）
python init_pgvector.py               # 初始化向量表
uvicorn app.main:app --reload --port 8000

# 前端
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`，默认账号 `admin / admin123`。

## 部署

| 方式 | 文档 | 适用场景 |
|------|------|---------|
| 手动部署 | [02-手动部署指南](docs/02-手动部署指南.md) | 完全控制，适合已有 Linux 服务器 |
| Docker 部署 | [03-Docker部署指南](docs/03-Docker部署指南.md) | 一键启动，快速部署 |
| pgvector 安装 | [04-pgvector安装指南](docs/04-pgvector安装指南.md) | RAG 向量数据库部署 |

## 文档索引

| 编号 | 文档 | 说明 |
|------|------|------|
| 01 | [本地开发指南](docs/01-本地开发指南.md) | 本地环境搭建、首次配置、启动流程 |
| 02 | [手动部署指南](docs/02-手动部署指南.md) | Linux 手动部署、systemd、Nginx、HTTPS |
| 03 | [Docker部署指南](docs/03-Docker部署指南.md) | Docker Compose 容器化部署 |
| 04 | [pgvector安装指南](docs/04-pgvector安装指南.md) | PostgreSQL + pgvector 安装 |
| 05 | [AI开发助手注记](docs/05-AI开发助手注记.md) | AI 编码助手上下文（AGENTS.md） |

## License

MIT
