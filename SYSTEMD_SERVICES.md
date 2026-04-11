# AgenticOps Linux systemd 服务模板

本文提供可直接落地的 3 个 systemd 服务（API / Celery Worker / Celery Beat），默认部署路径为 `/opt/AgenticOps`。

## 1) `agenticops-api.service`

将以下内容保存为 `/etc/systemd/system/agenticops-api.service`：

```ini
[Unit]
Description=AgenticOps FastAPI Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/AgenticOps/backend
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/AgenticOps/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 2) `agenticops-celery-worker.service`

将以下内容保存为 `/etc/systemd/system/agenticops-celery-worker.service`：

```ini
[Unit]
Description=AgenticOps Celery Worker
After=network.target redis.service
Requires=redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/AgenticOps/backend
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/AgenticOps/backend/.venv/bin/celery -A celery_app worker --loglevel=info -Q salt,scheduler
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 3) `agenticops-celery-beat.service`

将以下内容保存为 `/etc/systemd/system/agenticops-celery-beat.service`：

```ini
[Unit]
Description=AgenticOps Celery Beat
After=network.target redis.service
Requires=redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/AgenticOps/backend
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/AgenticOps/backend/.venv/bin/celery -A celery_app beat --loglevel=info
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 4) 启用与管理

```bash
sudo systemctl daemon-reload

sudo systemctl enable --now agenticops-api
sudo systemctl enable --now agenticops-celery-worker
sudo systemctl enable --now agenticops-celery-beat

sudo systemctl status agenticops-api
sudo systemctl status agenticops-celery-worker
sudo systemctl status agenticops-celery-beat
```

## 5) 常用排障命令

```bash
# 查看实时日志
journalctl -u agenticops-api -f
journalctl -u agenticops-celery-worker -f
journalctl -u agenticops-celery-beat -f

# 重启服务
sudo systemctl restart agenticops-api
sudo systemctl restart agenticops-celery-worker
sudo systemctl restart agenticops-celery-beat
```

## 6) 部署前检查

- `/opt/AgenticOps/backend/config.yaml` 已存在且配置正确。
- 虚拟环境和依赖已安装：`/opt/AgenticOps/backend/.venv`。
- Redis 已启动并可连接。
- 若从旧版升级，已执行一次：`python /opt/AgenticOps/backend/add_server_menu.py`。

## 7) 说明

- 后端建议固定运行在 `8000`，与前端 `/api` 代理约定一致。
- 任务调度依赖 `worker + beat` 同时在线。
- 首次初始化数据库会清空旧数据：`python init_db.py`，生产环境慎用。
