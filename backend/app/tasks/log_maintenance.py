"""执行日志归档与清理任务"""

import asyncio
import logging
import re
from datetime import datetime, timedelta

from celery_app import celery_app
from sqlalchemy import delete, select, text

from app.core import config
from app.db.database import AsyncSessionLocal
from app.models.ops import TaskExecutionLog

logger = logging.getLogger(__name__)

_MAINTAIN_LOOP = None
_TABLE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


def _run_async(coro):
    global _MAINTAIN_LOOP
    if _MAINTAIN_LOOP is None or _MAINTAIN_LOOP.is_closed():
        _MAINTAIN_LOOP = asyncio.new_event_loop()
    return _MAINTAIN_LOOP.run_until_complete(coro)


def _get_cleanup_settings() -> dict:
    return {
        "enabled": bool(config._get("ops", "logs", "cleanup", "enabled", default=True)),
        "retention_days": int(config._get("ops", "logs", "cleanup", "retention_days", default=90) or 90),
        "batch_size": int(config._get("ops", "logs", "cleanup", "batch_size", default=2000) or 2000),
        "max_batches": int(config._get("ops", "logs", "cleanup", "max_batches", default=20) or 20),
        "archive_enabled": bool(config._get("ops", "logs", "cleanup", "archive_enabled", default=True)),
        "archive_table": str(
            config._get("ops", "logs", "cleanup", "archive_table", default="ops_task_execution_log_archive")
            or "ops_task_execution_log_archive"
        ),
    }


def _safe_archive_table_name(raw_name: str) -> str:
    if _TABLE_NAME_PATTERN.match(raw_name):
        return raw_name
    logger.warning("archive_table 配置非法，回退默认值: %s", raw_name)
    return "ops_task_execution_log_archive"


async def _ensure_archive_table(db, table_name: str) -> None:
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
      `id` BIGINT NOT NULL AUTO_INCREMENT,
      `original_log_id` BIGINT NOT NULL,
      `task_id` INT NULL,
      `server_id` INT NULL,
      `status` VARCHAR(20) NULL,
      `command` LONGTEXT NOT NULL,
      `output` LONGTEXT NULL,
      `error` LONGTEXT NULL,
      `exit_code` INT NULL,
      `started_at` DATETIME NULL,
      `finished_at` DATETIME NULL,
      `duration` FLOAT NULL,
      `created_at` DATETIME NULL,
      `archived_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `uk_original_log_id` (`original_log_id`),
      KEY `idx_created_at` (`created_at`),
      KEY `idx_status_created_at` (`status`, `created_at`),
      KEY `idx_task_created_at` (`task_id`, `created_at`),
      KEY `idx_server_created_at` (`server_id`, `created_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    await db.execute(text(create_sql))


async def _archive_and_cleanup_logs_async() -> dict:
    settings = _get_cleanup_settings()
    if not settings["enabled"]:
        return {"status": "skipped", "reason": "cleanup disabled"}

    retention_days = max(settings["retention_days"], 1)
    batch_size = max(settings["batch_size"], 100)
    max_batches = max(settings["max_batches"], 1)
    archive_enabled = settings["archive_enabled"]
    archive_table = _safe_archive_table_name(settings["archive_table"])
    cutoff_time = datetime.now() - timedelta(days=retention_days)

    archived_total = 0
    deleted_total = 0
    batch_executed = 0

    async with AsyncSessionLocal() as db:
        if archive_enabled:
            await _ensure_archive_table(db, archive_table)
            await db.commit()

        for _ in range(max_batches):
            ids_result = await db.execute(
                select(TaskExecutionLog.id)
                .where(TaskExecutionLog.created_at < cutoff_time)
                .order_by(TaskExecutionLog.id.asc())
                .limit(batch_size)
            )
            ids = [row[0] for row in ids_result.fetchall()]
            if not ids:
                break

            id_list_sql = ",".join(str(log_id) for log_id in ids)

            if archive_enabled:
                archive_sql = f"""
                INSERT IGNORE INTO `{archive_table}`
                    (`original_log_id`, `task_id`, `server_id`, `status`, `command`, `output`, `error`,
                     `exit_code`, `started_at`, `finished_at`, `duration`, `created_at`)
                SELECT
                    `id`, `task_id`, `server_id`, `status`, `command`, `output`, `error`,
                    `exit_code`, `started_at`, `finished_at`, `duration`, `created_at`
                FROM `ops_task_execution_log`
                WHERE `id` IN ({id_list_sql})
                """
                archive_result = await db.execute(text(archive_sql))
                archived_total += int(archive_result.rowcount or 0)

            await db.execute(delete(TaskExecutionLog).where(TaskExecutionLog.id.in_(ids)))
            deleted_total += len(ids)
            batch_executed += 1
            await db.commit()

    return {
        "status": "success",
        "retention_days": retention_days,
        "cutoff_time": cutoff_time.isoformat(),
        "batch_size": batch_size,
        "max_batches": max_batches,
        "batches": batch_executed,
        "archive_enabled": archive_enabled,
        "archive_table": archive_table if archive_enabled else None,
        "archived": archived_total,
        "deleted": deleted_total,
    }


@celery_app.task(queue="scheduler")
def archive_and_cleanup_execution_logs():
    """按配置归档并清理历史执行日志。"""
    try:
        result = _run_async(_archive_and_cleanup_logs_async())
        logger.info("执行日志归档清理完成: %s", result)
        return result
    except Exception as exc:
        logger.error("执行日志归档清理失败: %s", exc)
        return {
            "status": "failed",
            "error": str(exc),
        }
