"""Celery 应用配置"""

import asyncio
import sys

from celery import Celery
from celery.schedules import crontab
from app.core import config

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 获取 Redis 配置
redis_config = config._get("redis", default={}).get("default", {})
redis_host = redis_config.get("host", "localhost")
redis_port = redis_config.get("port", 6379)
redis_password = redis_config.get("password", "")
redis_db_broker = redis_config.get("db", 1)
redis_db_backend = redis_config.get("db", 2)

# 构建 Redis URL
if redis_password:
    broker_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db_broker}"
    result_backend = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db_backend}"
else:
    broker_url = f"redis://{redis_host}:{redis_port}/{redis_db_broker}"
    result_backend = f"redis://{redis_host}:{redis_port}/{redis_db_backend}"

# 创建 Celery 实例
celery_app = Celery(
    "agentic_ops",
    broker=broker_url,
    backend=result_backend,
    include=[
        "app.tasks.salt_tasks",
        "app.tasks.jumpserver_tasks",
        "app.tasks.scheduler",
        "app.tasks.log_maintenance",
    ],
)

cleanup_enabled = bool(config._get("ops", "logs", "cleanup", "enabled", default=True))
cleanup_hour = int(config._get("ops", "logs", "cleanup", "run_hour", default=3) or 3)
cleanup_minute = int(config._get("ops", "logs", "cleanup", "run_minute", default=10) or 10)

beat_schedule = {
    "check-scheduled-tasks": {
        "task": "app.tasks.scheduler.check_and_execute_tasks",
        "schedule": 60.0,
    },
}

if cleanup_enabled:
    beat_schedule["archive-and-cleanup-execution-logs"] = {
        "task": "app.tasks.log_maintenance.archive_and_cleanup_execution_logs",
        "schedule": crontab(hour=cleanup_hour, minute=cleanup_minute),
    }

# Celery 配置
celery_app.conf.update(
    timezone="Asia/Shanghai",
    enable_utc=True,
    
    # 任务序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # 并发配置
    worker_concurrency=4,
    worker_prefetch_multiplier=1,
    
    # 任务超时
    task_soft_time_limit=300,  # 5分钟软超时
    task_time_limit=600,  # 10分钟硬超时
    
    # 重试配置
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # 结果过期时间(24小时)
    result_expires=86400,
    
    # 定时任务配置
    beat_schedule=beat_schedule,
)

# 任务路由
celery_app.conf.task_routes = {
    "app.tasks.salt_tasks.*": {"queue": "salt"},
    "app.tasks.jumpserver_tasks.*": {"queue": "jumpserver"},
    "app.tasks.scheduler.*": {"queue": "scheduler"},
}

if __name__ == "__main__":
    celery_app.start()
