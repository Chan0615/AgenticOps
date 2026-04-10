"""定时任务 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.schemas.task import (
    ScheduledTaskCreate,
    ScheduledTaskUpdate,
    ScheduledTaskResponse,
    ScheduledTaskListResponse,
    TaskManualTriggerRequest,
)
from app.schemas.system.user import UserResponse
from app.crud.ops import task as task_crud
from app.api.auth.auth import get_current_user
from app.core.log_decorator import log_operation
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/tasks", tags=["定时任务"])


def _normalize_task_type(task_obj):
    if getattr(task_obj, "task_type", None) != "salt":
        task_obj.task_type = "salt"
    return task_obj


@router.get("", response_model=ScheduledTaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="任务名称"),
    enabled: Optional[bool] = Query(None, description="是否启用"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取定时任务列表"""
    skip = (page - 1) * page_size
    tasks, total = await task_crud.get_tasks(
        db, skip=skip, limit=page_size, name=name, enabled=enabled
    )
    normalized_tasks = [_normalize_task_type(t) for t in tasks]
    
    return ScheduledTaskListResponse(
        code=200,
        message="success",
        data=[ScheduledTaskResponse.model_validate(t) for t in normalized_tasks],
        total=total,
    )


@router.get("/{task_id}", response_model=ScheduledTaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取任务详情"""
    task = await task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    task = _normalize_task_type(task)
    return task


@router.post("", response_model=ScheduledTaskResponse)
@log_operation(module="运维-任务", action="创建任务", description="创建定时任务")
async def create_task(
    task: ScheduledTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """创建定时任务"""
    db_task = await task_crud.create_task(
        db, task, created_by=current_user.username
    )
    return db_task


@router.put("/{task_id}", response_model=ScheduledTaskResponse)
@log_operation(module="运维-任务", action="更新任务", description="更新定时任务")
async def update_task(
    task_id: int,
    task: ScheduledTaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """更新定时任务"""
    db_task = await task_crud.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return db_task


@router.delete("/{task_id}")
@log_operation(module="运维-任务", action="删除任务", description="删除定时任务")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """删除定时任务"""
    success = await task_crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"code": 200, "message": "删除成功"}


@router.post("/{task_id}/toggle")
@log_operation(module="运维-任务", action="切换任务状态", description="启用或禁用定时任务")
async def toggle_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """切换任务启用状态"""
    db_task = await task_crud.toggle_task_enabled(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "task_id": task_id,
            "enabled": db_task.enabled,
        },
    }


@router.post("/trigger")
@log_operation(module="运维-任务", action="手动触发任务", description="手动执行定时任务")
async def trigger_task(
    request: TaskManualTriggerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """手动触发任务执行"""
    task = await task_crud.get_task(db, request.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    from app.tasks.salt_tasks import execute_salt_command

    async_result = execute_salt_command.delay(task.id, task.server_ids or [], task.command or "")
    task.celery_task_id = async_result.id
    await db.commit()
     
    # 更新执行时间
    await task_crud.update_task_execution_time(db, request.task_id)
    
    return {
        "code": 200,
        "message": "任务已触发",
        "data": {
            "task_id": request.task_id,
            "celery_task_id": async_result.id,
        },
    }
