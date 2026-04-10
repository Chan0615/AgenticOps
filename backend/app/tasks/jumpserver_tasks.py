"""JumpServer 异步任务"""

import logging
from celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, queue="jumpserver")
def execute_jumpserver_command(self, task_id: int, server_id: int, command: str):
    """通过 JumpServer 执行命令（任务骨架）。"""
    try:
        logger.info(
            "开始执行 JumpServer 任务: task_id=%s, server_id=%s", task_id, server_id
        )
        return {
            "status": "pending",
            "message": "JumpServer 任务执行待接入具体作业 API",
            "task_id": task_id,
            "server_id": server_id,
            "command": command,
        }
    except Exception as e:
        logger.error("JumpServer 任务执行失败: %s", e)
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60)
        return {
            "status": "failed",
            "error": str(e),
            "task_id": task_id,
            "server_id": server_id,
        }
