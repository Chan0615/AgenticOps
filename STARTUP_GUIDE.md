# AgenticOps 启动与部署指南

## 1. 说明
- 后端统一入口是 `backend/app/main.py`，启动命令使用 `uvicorn app.main:app --port 8000`（在 `backend/` 下执行）。
- 前端入口是 `frontend/src/main.ts`，本地开发使用 Vite `5173`。
- `backend/config.yaml` 为必需文件，缺失会导致后端导入配置时报错。

## 2. 本地开发（Windows）

### 2.1 首次初始化
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
copy config.yaml.example config.yaml
python init_db.py
```

### 2.2 后端（窗口 1）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### 2.3 Celery Worker（窗口 2）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
.\.venv\Scripts\Activate.ps1
celery -A celery_app worker --loglevel=info -Q salt,scheduler -P solo
```

### 2.4 Celery Beat（窗口 3）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
.\.venv\Scripts\Activate.ps1
celery -A celery_app beat --loglevel=info
```

### 2.5 前端（窗口 4）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\frontend
npm install
npm run dev
```

### 2.6 验证
- 前端：`http://localhost:5173`
- 后端：`http://localhost:8000/docs`
- 默认账号：`admin / admin123`

## 3. Linux 服务器部署步骤（推荐 Ubuntu/CentOS）

### 3.1 安装依赖
```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip nodejs npm redis-server
```

### 3.2 拉取代码并准备后端
```bash
cd /opt
sudo git clone <your-repo-url> AgenticOps
sudo chown -R $USER:$USER /opt/AgenticOps

cd /opt/AgenticOps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.yaml.example config.yaml
```

### 3.3 配置 `backend/config.yaml`
- 必填数据库、Redis、SaltStack、JumpServer 配置。
- JumpServer 相关项需可用：`jumpserver.base_url`、认证字段、`org_id`。
- `config.yaml` 含环境敏感信息，不要提交到仓库。

### 3.4 初始化数据库（仅首次）
```bash
cd /opt/AgenticOps/backend
source .venv/bin/activate
python init_db.py
```

### 3.5 兼容旧数据（如从旧版升级）
```bash
cd /opt/AgenticOps/backend
source .venv/bin/activate
python add_server_menu.py
```

### 3.6 构建前端
```bash
cd /opt/AgenticOps/frontend
npm install
npm run build
```

### 3.7 启动后端与 Celery（临时启动）
```bash
cd /opt/AgenticOps/backend
source .venv/bin/activate

# API
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Worker（新终端）
celery -A celery_app worker --loglevel=info -Q salt,scheduler

# Beat（新终端）
celery -A celery_app beat --loglevel=info
```

### 3.8 systemd 托管（生产建议）
建议拆分 3 个服务：
- `agenticops-api.service`
- `agenticops-celery-worker.service`
- `agenticops-celery-beat.service`

完整可复制模板见：`SYSTEMD_SERVICES.md`

示例（API）：
```ini
[Unit]
Description=AgenticOps API
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/AgenticOps/backend
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/AgenticOps/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用：
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now agenticops-api
sudo systemctl enable --now agenticops-celery-worker
sudo systemctl enable --now agenticops-celery-beat
```

## 4. 运行检查清单
- `redis-server` 已启动且可连接。
- `backend/config.yaml` 存在且配置完整。
- `worker` 消费队列包含 `salt,scheduler`。
- 任务调度依赖 `worker + beat` 同时在线。
- 前端反向代理 `/api -> http://localhost:8000`（Vite 本地默认已配置）。

## 5. 风险提示
- `python backend/init_db.py` 默认会清空并重建数据库（生产环境慎用）。
- Windows 下 Celery 建议 `-P solo`，Linux 通常不需要。

## 6. 相关文档
- systemd 服务模板：`SYSTEMD_SERVICES.md`
- Nginx 反向代理与前端静态部署：`NGINX_DEPLOY.md`
