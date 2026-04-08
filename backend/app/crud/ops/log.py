"""执行日志 CRUD 操作"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops import TaskExecutionLog
import logging

logger = logging.getLogger(__name__)


async def get_execution_log(db: AsyncSession, log_id: int) -> Optional[TaskExecutionLog]:
    """根据ID获取执行日志"""
    result = await db.execute(select(TaskExecutionLog).where(TaskExecutionLog.id == log_id))
    return result.scalar_one_or_none()


async def get_execution_logs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    task_id: Optional[int] = None,
    server_id: Optional[int] = None,
    status: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> tuple[List[TaskExecutionLog], int]:
    """获取执行日志列表"""
    query = select(TaskExecutionLog)
    count_query = select(func.count(TaskExecutionLog.id))
    
    if task_id:
        query = query.where(TaskExecutionLog.task_id == task_id)
        count_query = count_query.where(TaskExecutionLog.task_id == task_id)
    
    if server_id:
        query = query.where(TaskExecutionLog.server_id == server_id)
        count_query = count_query.where(TaskExecutionLog.server_id == server_id)
    
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
