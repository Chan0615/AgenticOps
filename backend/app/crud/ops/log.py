"""执行日志 CRUD 操作"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, func, or_
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops import TaskExecutionLog, ScheduledTask, Server
import logging

logger = logging.getLogger(__name__)


async def get_execution_log(db: AsyncSession, log_id: int) -> Optional[TaskExecutionLog]:
    """根据ID获取执行日志"""
    result = await db.execute(
        select(TaskExecutionLog)
        .options(joinedload(TaskExecutionLog.task), joinedload(TaskExecutionLog.server))
        .where(TaskExecutionLog.id == log_id)
    )
    return result.scalar_one_or_none()


async def get_execution_logs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    task_id: Optional[int] = None,
    server_id: Optional[int] = None,
    task_name: Optional[str] = None,
    server_keyword: Optional[str] = None,
    status: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> tuple[List[TaskExecutionLog], int]:
    """获取执行日志列表"""
    query = (
        select(TaskExecutionLog)
        .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
        .outerjoin(Server, TaskExecutionLog.server_id == Server.id)
        .options(
            load_only(
                TaskExecutionLog.id,
                TaskExecutionLog.task_id,
                TaskExecutionLog.server_id,
                TaskExecutionLog.status,
                TaskExecutionLog.command,
                TaskExecutionLog.exit_code,
                TaskExecutionLog.started_at,
                TaskExecutionLog.finished_at,
                TaskExecutionLog.duration,
                TaskExecutionLog.created_at,
            ),
            joinedload(TaskExecutionLog.task).load_only(ScheduledTask.id, ScheduledTask.name),
            joinedload(TaskExecutionLog.server).load_only(Server.id, Server.hostname, Server.name),
        )
    )
    count_query = (
        select(func.count(TaskExecutionLog.id))
        .select_from(TaskExecutionLog)
        .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
        .outerjoin(Server, TaskExecutionLog.server_id == Server.id)
    )
    
    if task_id:
        query = query.where(TaskExecutionLog.task_id == task_id)
        count_query = count_query.where(TaskExecutionLog.task_id == task_id)
    
    if server_id:
        query = query.where(TaskExecutionLog.server_id == server_id)
        count_query = count_query.where(TaskExecutionLog.server_id == server_id)

    if task_name:
        query = query.where(ScheduledTask.name.ilike(f"%{task_name}%"))
        count_query = count_query.where(ScheduledTask.name.ilike(f"%{task_name}%"))

    if server_keyword:
        server_filter = or_(
            Server.hostname.ilike(f"%{server_keyword}%"),
            Server.name.ilike(f"%{server_keyword}%"),
        )
        query = query.where(server_filter)
        count_query = count_query.where(server_filter)
    
    if status:
        query = query.where(TaskExecutionLog.status == status)
        count_query = count_query.where(TaskExecutionLog.status == status)
    
    if start_time:
        query = query.where(TaskExecutionLog.created_at >= start_time)
        count_query = count_query.where(TaskExecutionLog.created_at >= start_time)
    
    if end_time:
        query = query.where(TaskExecutionLog.created_at <= end_time)
        count_query = count_query.where(TaskExecutionLog.created_at <= end_time)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset(skip).limit(limit).order_by(TaskExecutionLog.created_at.desc())
    result = await db.execute(query)
    logs = result.scalars().all()
    
    return logs, total


async def create_execution_log(
    db: AsyncSession,
    task_id: Optional[int],
    server_id: Optional[int],
    command: str,
    status: str = "pending",
    output: Optional[str] = None,
    error: Optional[str] = None,
    exit_code: Optional[int] = None,
    started_at: Optional[datetime] = None,
    finished_at: Optional[datetime] = None,
    duration: Optional[float] = None,
) -> TaskExecutionLog:
    """创建执行日志"""
    db_log = TaskExecutionLog(
        task_id=task_id,
        server_id=server_id,
        command=command,
        status=status,
        output=output,
        error=error,
        exit_code=exit_code,
        started_at=started_at,
        finished_at=finished_at,
        duration=duration,
    )
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log


async def update_execution_log(
    db: AsyncSession,
    log_id: int,
    status: Optional[str] = None,
    output: Optional[str] = None,
    error: Optional[str] = None,
    exit_code: Optional[int] = None,
    finished_at: Optional[datetime] = None,
    duration: Optional[float] = None,
) -> Optional[TaskExecutionLog]:
    """更新执行日志"""
    db_log = await get_execution_log(db, log_id)
    if not db_log:
        return None
    
    if status:
        db_log.status = status
    if output:
        db_log.output = output
    if error:
        db_log.error = error
    if exit_code is not None:
        db_log.exit_code = exit_code
    if finished_at:
        db_log.finished_at = finished_at
    if duration:
        db_log.duration = duration
    
    await db.commit()
    await db.refresh(db_log)
    return db_log
