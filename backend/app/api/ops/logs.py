"""执行日志 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime, timedelta
from app.db.database import get_db
from app.schemas.log import (
    TaskExecutionLogResponse,
    TaskExecutionLogListResponse,
)
from app.crud.ops import log as log_crud
from app.api.auth.auth import get_current_user
from app.core import config
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/logs", tags=["执行日志"])
DEFAULT_RECENT_DAYS = int(config._get("ops", "logs", "default_recent_days", default=30) or 30)


def _to_execution_log_response(log, include_content: bool = True) -> TaskExecutionLogResponse:
    output = log.output if include_content else log.__dict__.get("output")
    error = log.error if include_content else log.__dict__.get("error")
    return TaskExecutionLogResponse(
        id=log.id,
        task_id=log.task_id,
        task_name=getattr(log.task, "name", None) if getattr(log, "task", None) else None,
        server_id=log.server_id,
        server_ip=getattr(log.server, "hostname", None) if getattr(log, "server", None) else None,
        status=log.status,
        command=log.command,
        output=output,
        error=error,
        exit_code=log.exit_code,
        started_at=log.started_at,
        finished_at=log.finished_at,
        duration=log.duration,
        created_at=log.created_at,
    )


@router.get("/execution", response_model=TaskExecutionLogListResponse)
async def list_execution_logs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    task_id: Optional[int] = Query(None, description="任务ID"),
    server_id: Optional[int] = Query(None, description="服务器ID"),
    task_name: Optional[str] = Query(None, description="任务名称"),
    server_keyword: Optional[str] = Query(None, description="服务器IP或名称关键字"),
    status: Optional[str] = Query(None, description="状态"),
    recent_days: Optional[int] = Query(
        None, ge=0, le=3650, description="最近N天（0表示不过滤）"
    ),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取执行日志列表"""
    if start_time is None and end_time is None:
        effective_recent_days = DEFAULT_RECENT_DAYS if recent_days is None else recent_days
        if effective_recent_days > 0:
            start_time = datetime.now() - timedelta(days=effective_recent_days)

    skip = (page - 1) * page_size
    logs, total = await log_crud.get_execution_logs(
        db,
        skip=skip,
        limit=page_size,
        task_id=task_id,
        server_id=server_id,
        task_name=task_name,
        server_keyword=server_keyword,
        status=status,
        start_time=start_time,
        end_time=end_time,
    )
    
    return TaskExecutionLogListResponse(
        code=200,
        message="success",
        data=[_to_execution_log_response(log, include_content=False) for log in logs],
        total=total,
    )


@router.get("/execution/{log_id}", response_model=TaskExecutionLogResponse)
async def get_execution_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取执行日志详情"""
    log = await log_crud.get_execution_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    return _to_execution_log_response(log)
