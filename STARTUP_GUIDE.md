# AgenticOps 服务启动指南

## 目标
- 只保留一份启动文档，覆盖本地开发最常用流程。

## 后端（窗口 1）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

## Celery Worker（窗口 2）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
.\.venv\Scripts\Activate.ps1
celery -A celery_app worker --loglevel=info -Q salt,scheduler -P solo
```

## Celery Beat（窗口 3）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
.\.venv\Scripts\Activate.ps1
celery -A celery_app beat --loglevel=info
```

## 前端（窗口 4）
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\frontend
npm install
npm run dev
```

## 首次初始化
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
copy config.yaml.example config.yaml
python init_db.py
```

## 验证
- 前端: `http://localhost:5173`
- 后端: `http://localhost:8000/docs`
- 默认账号: `admin / admin123`

## 注意
- `python backend/init_db.py` 默认会清空并重建数据库。
- 定时任务与手动触发依赖 Worker + Beat 同时运行。
- Windows 下 Celery 建议使用 `-P solo`，避免 `billiard` 多进程 `PermissionError: [WinError 5]`。
