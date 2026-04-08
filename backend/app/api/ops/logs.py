"""执行日志 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app.db.database import get_db
from app.schemas.log import (
    TaskExecutionLogResponse,
    TaskExecutionLogListResponse,
)
from app.crud.ops import log as log_crud
from app.api.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/logs", tags=["执行日志"])


@router.get("/execution", response_model=TaskExecutionLogListResponse)
async def list_execution_logs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    task_id: Optional[int] = Query(None, description="任务ID"),
    server_id: Optional[int] = Query(None, description="服务器ID"),
    status: Optional[str] = Query(None, description="状态"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取执行日志列表"""
    skip = (page - 1) * page_size
    logs, total = await log_crud.get_execution_logs(
        db,
        skip=skip,
        limit=page_size,
        task_id=task_id,
        server_id=server_id,
        status=status,
        start_time=start_time,
        end_time=end_time,
    )
    
    return TaskExecutionLogListResponse(
        code=200,
        message="success",
        data=[TaskExecutionLogResponse.model_validate(log) for log in logs],
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
    return log
