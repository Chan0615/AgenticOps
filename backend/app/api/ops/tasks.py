"""定时任务 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.schemas.task import (
    CronNaturalConvertRequest,
    CronNaturalConvertResponse,
    CronPreviewRequest,
    CronPreviewResponse,
    CronValidateRequest,
    CronValidationResponse,
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
from app.services.cron_helper import (
    describe_cron_zh,
    natural_to_cron,
    preview_next_runs,
    validate_cron,
)
from celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/tasks", tags=["定时任务"])


@router.post("/cron/validate", response_model=CronValidationResponse)
async def validate_task_cron(
    request: CronValidateRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    cron_expression = request.cron_expression.strip()
    valid, error = validate_cron(cron_expression)
    if valid:
        return {
            "code": 200,
            "message": "success",
            "data": {
                "valid": True,
                "cron_expression": cron_expression,
                "description_zh": describe_cron_zh(cron_expression),
                "error": None,
            },
        }

    return {
        "code": 200,
        "message": "success",
        "data": {
            "valid": False,
            "cron_expression": cron_expression,
            "description_zh": None,
            "error": error,
        },
    }


@router.post("/cron/describe", response_model=CronValidationResponse)
async def describe_task_cron(
    request: CronValidateRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    cron_expression = request.cron_expression.strip()
    valid, error = validate_cron(cron_expression)
    if not valid:
        return {
            "code": 200,
            "message": "success",
            "data": {
                "valid": False,
                "cron_expression": cron_expression,
                "description_zh": None,
                "error": error,
            },
        }

    return {
        "code": 200,
        "message": "success",
        "data": {
            "valid": True,
            "cron_expression": cron_expression,
            "description_zh": describe_cron_zh(cron_expression),
            "error": None,
        },
    }


@router.post("/cron/preview", response_model=CronPreviewResponse)
async def preview_task_cron(
    request: CronPreviewRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    cron_expression = request.cron_expression.strip()
    valid, error = validate_cron(cron_expression)
    if not valid:
        raise HTTPException(status_code=400, detail=error or "Cron表达式不合法")

    base_time = request.start_time or datetime.now()
    try:
        next_runs = preview_next_runs(
            cron_expression=cron_expression,
            count=request.count,
            start_time=base_time,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "code": 200,
        "message": "success",
        "data": {
            "cron_expression": cron_expression,
            "start_time": base_time,
            "next_runs": next_runs,
        },
    }


@router.post("/cron/natural", response_model=CronNaturalConvertResponse)
async def convert_natural_to_cron(
    request: CronNaturalConvertRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        cron_expression = natural_to_cron(request.text)
        valid, error = validate_cron(cron_expression)
        if not valid:
            raise ValueError(error or "转换后的 Cron 表达式不合法")
        description_zh = describe_cron_zh(cron_expression)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "code": 200,
        "message": "success",
        "data": {
            "text": request.text,
            "cron_expression": cron_expression,
            "description_zh": description_zh,
        },
    }


def _normalize_task_type(task_obj):
    if getattr(task_obj, "task_type", None) != "salt":
        task_obj.task_type = "salt"
    return task_obj


def _to_task_response(task_obj):
    task_obj = _normalize_task_type(task_obj)
    payload = ScheduledTaskResponse.model_validate(task_obj)
    payload.project_name = getattr(task_obj.project, "name", None) if getattr(task_obj, "project", None) else None
    payload.group_name = getattr(task_obj.group, "name", None) if getattr(task_obj, "group", None) else None
    return payload


def _ensure_celery_worker_available() -> None:
    try:
        inspector = celery_app.control.inspect(timeout=1)
        ping_result = inspector.ping() if inspector else None
    except Exception as exc:
        logger.error("Celery 连通性检查失败: %s", exc)
        raise HTTPException(status_code=503, detail="Celery 服务不可用，请确认 Redis/Celery 已启动")

    if not ping_result:
        raise HTTPException(status_code=503, detail="未检测到可用 Celery Worker，请先启动 worker")


def _collect_celery_health() -> dict:
    try:
        inspector = celery_app.control.inspect(timeout=2)
        ping_result = inspector.ping() if inspector else None
        active_queues = inspector.active_queues() if inspector else None
        stats = inspector.stats() if inspector else None
    except Exception as exc:
        logger.error("Celery 健康检查失败: %s", exc)
        return {
            "ok": False,
            "workers": [],
            "required_queues": ["salt", "scheduler"],
            "queue_consumers": {},
            "missing_queues": ["salt", "scheduler"],
            "beat_healthy": False,
            "detail": "Celery inspector 调用失败",
        }

    ping_result = ping_result or {}
    active_queues = active_queues or {}
    stats = stats or {}

    workers = sorted(set(list(ping_result.keys()) + list(active_queues.keys()) + list(stats.keys())))

    queue_consumers: dict[str, int] = {}
    for _, queues in active_queues.items():
        for queue_info in queues or []:
            qname = queue_info.get("name")
            if not qname:
                continue
            queue_consumers[qname] = queue_consumers.get(qname, 0) + 1

    required_queues = ["salt", "scheduler"]
    missing_queues = [q for q in required_queues if queue_consumers.get(q, 0) == 0]

    beat_healthy = queue_consumers.get("scheduler", 0) > 0
    ok = bool(workers) and not missing_queues

    return {
        "ok": ok,
        "workers": workers,
        "required_queues": required_queues,
        "queue_consumers": queue_consumers,
        "missing_queues": missing_queues,
        "beat_healthy": beat_healthy,
        "detail": "ok" if ok else "worker 或队列消费异常",
    }


@router.get("/health")
async def get_task_scheduler_health(
    current_user: UserResponse = Depends(get_current_user),
):
    """检查 Celery worker/队列健康状态。"""
    health = _collect_celery_health()
    return {
        "code": 200,
        "message": "success",
        "data": health,
    }


@router.post("/sync")
@log_operation(module="运维-任务", action="立即同步任务", description="手动触发一次调度扫描")
async def sync_scheduled_tasks(
    current_user: UserResponse = Depends(get_current_user),
):
    """手动触发一次 scheduler 检查流程。"""
    health = _collect_celery_health()
    if not health.get("workers"):
        raise HTTPException(status_code=503, detail="未检测到 Celery Worker，请先启动 worker")
    if "scheduler" in (health.get("missing_queues") or []):
        raise HTTPException(status_code=503, detail="未检测到 scheduler 队列消费者，请使用 -Q salt,scheduler 启动 worker")

    from app.tasks.scheduler import check_and_execute_tasks

    try:
        async_result = check_and_execute_tasks.delay()
    except Exception as exc:
        logger.error("触发任务同步失败: %s", exc)
        raise HTTPException(status_code=503, detail="调度扫描投递失败，Celery/Broker 不可用")

    return {
        "code": 200,
        "message": "同步任务已触发",
        "data": {
            "celery_task_id": async_result.id,
        },
    }


@router.get("", response_model=ScheduledTaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="任务名称"),
    enabled: Optional[bool] = Query(None, description="是否启用"),
    project_id: Optional[int] = Query(None, description="所属项目ID"),
    group_id: Optional[int] = Query(None, description="所属分组ID"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取定时任务列表"""
    skip = (page - 1) * page_size
    tasks, total = await task_crud.get_tasks(
        db,
        skip=skip,
        limit=page_size,
        name=name,
        enabled=enabled,
        project_id=project_id,
        group_id=group_id,
    )
    normalized_tasks = [_to_task_response(t) for t in tasks]
    
    return ScheduledTaskListResponse(
        code=200,
        message="success",
        data=normalized_tasks,
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
    return _to_task_response(task)


@router.post("", response_model=ScheduledTaskResponse)
@log_operation(module="运维-任务", action="创建任务", description="创建定时任务")
async def create_task(
    task: ScheduledTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """创建定时任务"""
    try:
        db_task = await task_crud.create_task(
            db, task, created_by=current_user.username
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
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
    try:
        db_task = await task_crud.update_task(
            db, task_id, task, updated_by=current_user.username
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
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
    db_task = await task_crud.toggle_task_enabled(
        db, task_id, updated_by=current_user.username
    )
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

    _ensure_celery_worker_available()
    
    from app.tasks.salt_tasks import execute_salt_command

    try:
        async_result = execute_salt_command.delay(task.id, task.server_ids or [], task.command or "")
    except Exception as exc:
        logger.error("任务触发失败 task_id=%s: %s", task.id, exc)
        raise HTTPException(status_code=503, detail="任务投递失败，Celery/Broker 不可用")

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
