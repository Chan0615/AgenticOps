"""操作日志 API（旧版，待迁移到 Ops 模块）"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.db.database import get_db
from app.crud.common import log as log_crud
from app.schemas.log import TaskExecutionLogResponse, TaskExecutionLogListResponse
from app.api.auth.auth import get_current_user
from app.schemas.system.user import UserResponse
from app.core.log_decorator import log_operation

router = APIRouter(prefix="/logs", tags=["操作日志"])


@router.get("", response_model=TaskExecutionLogListResponse)
@router.get("/", response_model=TaskExecutionLogListResponse)
async def get_operation_logs(
    skip: int = Query(0, ge=0, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    module: Optional[str] = Query(None, description="模块过滤"),
    username: Optional[str] = Query(None, description="用户过滤"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取操作日志列表"""
    # TODO: 迁移到 Ops 模块的日志系统
    return TaskExecutionLogListResponse(
        code=200,
        message="请迁移到 /api/ops/logs/execution",
        data=[],
        total=0,
    )
