"""定时任务调度器"""

import logging
from datetime import datetime

from celery_app import celery_app
from croniter import croniter
from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.ops import ScheduledTask
from app.tasks.salt_tasks import execute_salt_command
from app.tasks.async_runner import run_async

logger = logging.getLogger(__name__)

def should_execute_task(task: ScheduledTask, now: datetime) -> bool:
    if not task.enabled:
        return False
    if task.next_run_at:
        return task.next_run_at <= now
    return True


async def _check_and_execute_tasks_async():
    async with AsyncSessionLocal() as db:
        now = datetime.now()
        result = await db.execute(select(ScheduledTask).where(ScheduledTask.enabled == True))
        tasks = result.scalars().all()

        triggered = 0
        for task in tasks:
            if not should_execute_task(task, now):
                continue

            async_result = execute_salt_command.delay(
                task.id,
                task.server_ids or [],
                task.command or "",
            )

            task.celery_task_id = async_result.id
            task.last_run_at = now
            try:
                cron = croniter(task.cron_expression, now)
                task.next_run_at = cron.get_next(datetime)
            except Exception as e:
                logger.error("计算任务下次执行时间失败 task_id=%s: %s", task.id, e)

            triggered += 1

        await db.commit()
        return {
            "status": "success",
            "checked": len(tasks),
            "triggered": triggered,
            "checked_at": now.isoformat(),
        }


@celery_app.task(queue="scheduler")
def check_and_execute_tasks():
    """每分钟检查 enabled 任务并按 cron 触发执行。"""
    try:
        return run_async(_check_and_execute_tasks_async())
    except Exception as e:
        logger.error("检查定时任务失败: %s", e)
        return {
            "status": "failed",
            "error": str(e),
        }
