# AgenticOps 智能运维与知识库平台

基于 FastAPI + Vue 3 的一体化平台，覆盖系统权限、RAG 知识库、运维资产管理、脚本分发、定时任务与执行日志。

## 技术栈

### 后端
- FastAPI、Uvicorn
- SQLAlchemy 2.x（异步）+ MySQL（aiomysql）
- Redis + Celery（worker/beat）
- JWT（python-jose）认证
- YAML 配置中心（`backend/config.yaml`）
- RAG 相关：LangChain、FAISS、Sentence Transformers
- 运维集成：Salt、JumpServer API（连接验证与运维流程）

### 前端
- Vue 3 + TypeScript + Vite
- Ant Design Vue（已从 Arco 迁移）
- Pinia + Vue Router + Axios
- TailwindCSS（辅助样式）

## 已开发功能

### 系统管理
- 用户管理：用户 CRUD、状态控制
- 角色管理：角色权限绑定
- 菜单管理：菜单树、按钮权限、图标配置
- 登录/鉴权：JWT 登录与会话态管理

### 运维模块（`/api/ops/*`）
- 服务器管理：资产维护、连接测试
- 脚本管理：脚本上传、编辑、分发
- 定时任务：Cron 调度、启停与手动触发
- 执行日志：任务执行记录与结果查看
- 项目与分组：
  - 项目 CRUD（`/api/ops/projects`）
  - 分组 CRUD（`/api/ops/groups`）
  - 脚本/任务支持项目与分组维度过滤

### 知识库与助手
- RAG 知识库管理
- 聊天问答与系统助手页面

### 前端体验升级
- 运维与设置模块已迁移至 Ant Design Vue
- 登录页/个人页采用插画风视觉方案
- 菜单图标已支持下拉可选与预览

## 计划开发功能

- 更细粒度权限（按钮级、数据范围）
- 操作审计与安全追踪
- 运维看板与告警能力增强
- 任务编排与批量执行体验优化
- 更多 AI 辅助运维能力（建议、排障、解释）

## 项目结构

```text
AgenticOps/
├─ backend/
│  ├─ app/
│  │  ├─ api/           # auth / system / ops / rag 等路由
│  │  ├─ crud/
│  │  ├─ models/
│  │  ├─ schemas/
│  │  ├─ services/
│  │  └─ core/
│  ├─ config.yaml.example
│  ├─ init_db.py
│  └─ requirements.txt
└─ frontend/
   ├─ src/
   │  ├─ api/
   │  ├─ views/
   │  ├─ layouts/
   │  ├─ router/
   │  └─ stores/
   └─ package.json
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

# 首次：复制配置文件
cp config.yaml.example config.yaml

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（注意：该脚本默认会重建表，请先确认环境）
python init_db.py

# 启动 API
uvicorn app.main:app --reload --port 8000

# 新终端：启动 celery worker
celery -A celery_app worker --loglevel=info -Q salt,scheduler

# 新终端：启动 celery beat
celery -A celery_app beat --loglevel=info
```

### 2) 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问：`http://localhost:5173`

## 关键说明

- 后端本地入口建议使用：`backend/app/main.py`（命令：`uvicorn app.main:app --reload --port 8000`）
- `backend/config.yaml` 为本地配置文件，已 gitignore，请勿提交敏感信息
- 旧版 `/server/*` 路由已迁移到 `/ops/*`
- 旧 SSH WebSocket 本地直连能力已下线为兼容提示，运维连接主流程基于 JumpServer API

## 分页参数限制（避免 422）

后端对部分列表接口限制了 `page_size`，超过会返回 422：

- `/api/ops/servers`：`page_size <= 100`
- `/api/ops/scripts`：`page_size <= 100`
- `/api/ops/tasks`：`page_size <= 100`
- `/api/ops/logs/*`：`page_size <= 100`
- `/api/ops/projects`：`page_size <= 200`
- `/api/ops/groups`：建议 `page_size <= 200`

## 可用脚本

### 前端
- `npm run dev`：开发模式
- `npm run build`：生产构建
- `npm run typecheck`：类型检查

### 后端
- `python init_db.py`：初始化/重建数据库
- `python add_server_menu.py`：旧菜单 `/server/*` 迁移到 `/ops/*`
- `python add_ops_project_group.py`：项目/分组数据迁移脚本

## API 文档

后端启动后：
- Swagger：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

## License

MIT
