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
- 脚本版本管理：
  - 版本表与版本号自动递增（初始上传生成 `v1`）
  - 版本历史列表、版本内容查看
  - 版本对比（unified diff）
  - 一键回滚到指定版本（支持回滚备注）
- 定时任务：Cron 调度、启停与手动触发
- 执行日志：任务执行记录与结果查看
- 运维看板（Dashboard）：
  - 真实数据概览（用户、知识库、主机、任务、执行、会话）
  - 近 7 天执行/失败趋势图
  - 按项目/分组筛选下钻
  - 系统脉冲可跳转日志详情
  - 系统公告支持手工维护（CRUD）
- 项目与分组：
  - 项目 CRUD（`/api/ops/projects`）
  - 分组 CRUD（`/api/ops/groups`）
  - 脚本/任务支持项目与分组维度过滤
  - 系统默认项目/分组禁删（前后端双重保护）

### 知识库与助手
- RAG 知识库管理
- 聊天问答与系统助手页面

### 前端体验升级
- 运维与设置模块已迁移至 Ant Design Vue
- 登录页/个人页采用插画风视觉方案
- 菜单图标已支持下拉可选与预览
- 仪表盘支持插画风布局、快捷胶囊入口、AI 助手大入口
- 任务创建页执行方式优化：
  - 选择脚本且命令留空时自动执行（Python -> `python3`，Shell -> `bash`）
  - 脚本下拉展示源文件名（如 `xxx.py` / `xxx.sh`）

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
- 开发模式建议限制热重载目录，避免上传脚本触发后端自动重启：
  - `uvicorn app.main:app --reload --reload-dir app --port 8000`

## 脚本版本 API（新增）

- `GET /api/ops/scripts/{script_id}/versions`：版本列表
- `GET /api/ops/scripts/{script_id}/versions/{version_id}`：版本详情（含脚本内容）
- `GET /api/ops/scripts/{script_id}/versions/compare`：版本对比
  - 参数：`from_version_id`、`to_version_id`
- `POST /api/ops/scripts/{script_id}/rollback`：回滚版本
  - body: `{"version_id": 12, "note": "回滚到稳定版本"}`

## 运维看板 API（新增）

- `GET /api/ops/dashboard/overview`：看板概览（支持筛选）
  - query: `project_id`、`group_id`
- `GET /api/ops/dashboard/notices`：公告列表
- `POST /api/ops/dashboard/notices`：新增公告
  - body: `{"title": "计划维护", "content": "周日 02:00-03:00", "enabled": true}`
- `PUT /api/ops/dashboard/notices/{notice_id}`：更新公告
- `DELETE /api/ops/dashboard/notices/{notice_id}`：删除公告

公告默认使用本地文件持久化：`backend/data/dashboard_notices.json`

## 任务执行规则（当前）

- 有 `command`：优先执行 `command`
- 无 `command` 且有 `script_id`：自动从脚本生成执行命令
  - Python 脚本：使用 `python3` 执行
  - Shell 脚本：使用 `bash` 执行
- 两者都为空：任务校验失败，不允许创建

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

## 下一步建议（可直接排期）

- 凭据中心（主机凭据加密、轮换、权限隔离）
- 运维审批流（高风险任务强制审批）
- 任务模板库（重启、巡检、清理、发布）
- 告警中心（阈值、通知渠道、告警收敛）
- 主机自动发现与 CMDB/云资源同步
- 任务批量编排（分批执行、并发控制、失败回滚）

## API 文档

后端启动后：
- Swagger：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

## License

MIT
