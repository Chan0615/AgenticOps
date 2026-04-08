"""操作日志 API"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.db.database import get_db
from app.crud.common import log as log_crud
from app.schemas.server.server import OperationLogResponse, OperationLogListResponse
from app.api.auth.auth import get_current_user
from app.schemas.system.user import UserResponse
from app.core.log_decorator import log_operation

router = APIRouter(prefix="/logs", tags=["操作日志"])


@router.get("/", response_model=OperationLogListResponse)
async def get_operation_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    module: Optional[str] = Query(None, description="模块过滤"),
    username: Optional[str] = Query(None, description="用户过滤"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取操作日志列表"""
    # 只有管理员可以查看所有日志
    if not current_user.is_superuser:
        # 普通用户只能查看自己的日志
        username = current_user.username
    
    logs = await log_crud.get_logs(
        db=db,
        module=module,
        username=username,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit,
    )
    
    # 获取总数
    all_logs = await log_crud.get_logs(
        db=db,
        module=module,
        username=username,
        start_time=start_time,
        end_time=end_time,
        skip=0,
        limit=10000,
    )
    
    return OperationLogListResponse(
        total=len(all_logs),
        items=[OperationLogResponse.model_validate(log) for log in logs],
    )


@router.get("/{log_id}", response_model=OperationLogResponse)
async def get_operation_log(
    log_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取操作日志详情"""
    log = await log_crud.get_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    
    # 只有管理员或日志所有者可以查看
    if not current_user.is_superuser and log.username != current_user.username:
        raise HTTPException(status_code=403, detail="没有权限查看此日志")
    
    return OperationLogResponse.model_validate(log)
