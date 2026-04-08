"""操作日志 CRUD"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from datetime import datetime
from app.models.log import OperationLog


async def create_log(
    db: AsyncSession,
    module: str,
    action: str,
    description: Optional[str] = None,
    user_id: Optional[int] = None,
    username: Optional[str] = None,
    method: Optional[str] = None,
    path: Optional[str] = None,
    status_code: Optional[int] = None,
    request_params: Optional[dict] = None,
    response_data: Optional[dict] = None,
    error_message: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    execution_time: Optional[int] = None,
) -> OperationLog:
    """创建操作日志"""
    log = OperationLog(
        user_id=user_id,
        username=username,
        module=module,
        action=action,
        description=description,
        method=method,
        path=path,
        status_code=status_code,
        request_params=request_params,
        response_data=response_data,
        error_message=error_message,
        ip_address=ip_address,
        user_agent=user_agent,
        execution_time=execution_time,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def get_logs(
    db: AsyncSession,
    module: Optional[str] = None,
    username: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[OperationLog]:
    """获取操作日志列表"""
    query = select(OperationLog)
    
    if module:
        query = query.where(OperationLog.module == module)
    if username:
        query = query.where(OperationLog.username == username)
    if start_time:
        query = query.where(OperationLog.created_at >= start_time)
    if end_time:
        query = query.where(OperationLog.created_at <= end_time)
    
    query = query.order_by(desc(OperationLog.created_at))
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_log_by_id(db: AsyncSession, log_id: int) -> Optional[OperationLog]:
    """根据ID获取日志"""
    result = await db.execute(
        select(OperationLog).where(OperationLog.id == log_id)
    )
    return result.scalar_one_or_none()
