"""SaltStack 异步任务"""

import logging
from datetime import datetime
from pathlib import Path

from celery_app import celery_app
from app.db.database import AsyncSessionLocal
from app.models.ops import ScheduledTask, Server, TaskExecutionLog, Script
from app.services.salt_service import salt_service
from app.tasks.async_runner import run_async
from sqlalchemy import select

logger = logging.getLogger(__name__)

DEFAULT_REMOTE_SCRIPT_DIR = "/root/ChAn"
MAX_FAILURE_LOG_CHARS = 2048


def _truncate_text(text: str, max_chars: int = MAX_FAILURE_LOG_CHARS) -> str:
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}\n... (truncated, total={len(text)} chars)"


def _build_failure_error(stderr: str, stdout: str) -> str:
    raw_error = (stderr or "").strip() or (stdout or "").strip() or "执行失败"
    return _truncate_text(raw_error)

def _parse_run_all_result(output) -> tuple[bool, int, str, str]:
    if isinstance(output, dict):
        retcode = int(output.get("retcode", 1))
        stdout = str(output.get("stdout", ""))
        stderr = str(output.get("stderr", ""))
        return retcode == 0, retcode, stdout, stderr

    text = "" if output is None else str(output)
    failed_keys = [
        "Traceback",
        "ERROR",
        "No minions matched",
        "AuthenticationError",
        "can't open file",
        "[Errno",
    ]
    success = text != "" and not any(key in text for key in failed_keys)
    return success, 0 if success else 1, text, "" if success else text


async def _resolve_command(db, task_id: int, command: str) -> str:
    if command and str(command).strip():
        return command

    task_result = await db.execute(select(ScheduledTask).where(ScheduledTask.id == task_id))
    task = task_result.scalar_one_or_none()
    if not task or not task.script_id:
        raise RuntimeError("任务缺少可执行命令，且未关联脚本")

    script_result = await db.execute(select(Script).where(Script.id == task.script_id))
    script = script_result.scalar_one_or_none()
    if not script:
        raise RuntimeError("关联脚本不存在")

    script_source = (script.content or "").strip()
    if not script_source:
        raise RuntimeError("关联脚本内容为空")

    source_name = Path(script_source).name if script_source else ""
    if not source_name:
        suffix = ".py" if script.script_type == "python" else ".sh"
        source_name = f"{script.name}{suffix}"

    remote_path = f"{DEFAULT_REMOTE_SCRIPT_DIR.rstrip('/')}/{source_name}"
    if script.script_type == "python":
        return f"python3 '{remote_path}'"
    return f"bash '{remote_path}'"


async def _execute_salt_command_async(task_id: int, server_ids: list[int], command: str):
    async with AsyncSessionLocal() as db:
        try:
            final_command = await _resolve_command(db, task_id, command)
        except Exception as e:
            now = datetime.now()
            for sid in server_ids or [None]:
                db.add(
                    TaskExecutionLog(
                        task_id=task_id,
                        server_id=sid,
                        status="failed",
                        command=command or "",
                        error=str(e),
                        exit_code=1,
                        started_at=now,
                        finished_at=now,
                        duration=0,
                    )
                )
            await db.commit()
            raise

        server_result = await db.execute(select(Server).where(Server.id.in_(server_ids)))
        servers = server_result.scalars().all()
        if not servers:
            raise RuntimeError("未找到目标服务器")

        summaries = []
        for server in servers:
            target = server.salt_minion_id or server.hostname
            if not target:
                summaries.append(
                    {
                        "server_id": server.id,
                        "server": server.hostname,
                        "server_name": server.name,
                        "target": target,
                        "status": "failed",
                        "error": "缺少 salt_minion_id 或 hostname",
                    }
                )
                continue

            started_at = datetime.now()
            log = TaskExecutionLog(
                task_id=task_id,
                server_id=server.id,
                status="running",
                command=final_command,
                started_at=started_at,
            )
            db.add(log)
            await db.commit()
            await db.refresh(log)

            try:
                result = await salt_service.run_command(
                    env_name=server.environment,
                    target=target,
                    fun="cmd.run_all",
                    arg=[final_command],
                )
                returns = result.get("return", []) if isinstance(result, dict) else []
                data_map = returns[0] if returns and isinstance(returns[0], dict) else {}
                output = data_map.get(target)
                if output is None and data_map:
                    output = next(iter(data_map.values()))

                is_success, exit_code, stdout, stderr = _parse_run_all_result(output)

                finished_at = datetime.now()
                log.status = "success" if is_success else "failed"
                log.output = None
                log.error = None if is_success else _build_failure_error(stderr, stdout)
                log.exit_code = exit_code
                log.finished_at = finished_at
                log.duration = (finished_at - started_at).total_seconds()
                await db.commit()

                summaries.append(
                    {
                        "server_id": server.id,
                        "server": server.hostname,
                        "server_name": server.name,
                        "target": target,
                        "status": log.status,
                    }
                )
            except Exception as e:
                finished_at = datetime.now()
                log.status = "failed"
                log.error = str(e)
                log.exit_code = 1
                log.finished_at = finished_at
                log.duration = (finished_at - started_at).total_seconds()
                await db.commit()

                summaries.append(
                    {
                        "server_id": server.id,
                        "server": server.hostname,
                        "server_name": server.name,
                        "target": target,
                        "status": "failed",
                        "error": str(e),
                    }
                )

        return summaries


@celery_app.task(bind=True, max_retries=3, queue="salt")
def execute_salt_command(self, task_id: int, server_ids: list, command: str):
    """通过 SaltStack 执行命令并写入执行日志。"""
    try:
        logger.info("开始执行 Salt 任务: task_id=%s, servers=%s", task_id, server_ids)
        summaries = run_async(_execute_salt_command_async(task_id, server_ids, command))
        success_count = sum(1 for item in summaries if item.get("status") == "success")
        failed_count = len(summaries) - success_count
        if failed_count == 0:
            task_status = "success"
        elif success_count == 0:
            task_status = "failed"
        else:
            task_status = "partial_failed"

        logger.info(
            "Salt 任务执行完成: task_id=%s, success=%s, failed=%s, status=%s",
            task_id,
            success_count,
            failed_count,
            task_status,
        )
        return {
            "status": task_status,
            "task_id": task_id,
            "success_count": success_count,
            "failed_count": failed_count,
            "results": summaries,
        }
    except Exception as e:
        logger.error("Salt 任务执行失败: %s", e)
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60)
        return {
            "status": "failed",
            "task_id": task_id,
            "error": str(e),
        }


@celery_app.task(bind=True, max_retries=3, queue="salt")
def test_salt_connection(self, salt_env: str = "fuchunyun", target: str = "*"):
    """测试 Salt 连接。"""
    try:
        result = run_async(salt_service.test_ping(env_name=salt_env, target=target))
        return result
    except Exception as e:
        logger.error("Salt 连接测试失败: %s", e)
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=30)
        raise
