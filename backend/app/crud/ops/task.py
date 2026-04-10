"""定时任务 CRUD 操作"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops import ScheduledTask
from app.schemas.task import ScheduledTaskCreate, ScheduledTaskUpdate
import logging

logger = logging.getLogger(__name__)


async def get_task(db: AsyncSession, task_id: int) -> Optional[ScheduledTask]:
    """根据ID获取任务"""
    result = await db.execute(select(ScheduledTask).where(ScheduledTask.id == task_id))
    return result.scalar_one_or_none()


async def get_tasks(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = None,
    enabled: Optional[bool] = None,
) -> tuple[List[ScheduledTask], int]:
    """获取任务列表"""
    query = select(ScheduledTask)
    count_query = select(func.count(ScheduledTask.id))
    
    if name:
        query = query.where(ScheduledTask.name.ilike(f"%{name}%"))
        count_query = count_query.where(ScheduledTask.name.ilike(f"%{name}%"))
    
    if enabled is not None:
        query = query.where(ScheduledTask.enabled == enabled)
        count_query = count_query.where(ScheduledTask.enabled == enabled)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset(skip).limit(limit).order_by(ScheduledTask.created_at.desc())
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return tasks, total


async def create_task(
    db: AsyncSession, task: ScheduledTaskCreate, created_by: str = None
) -> ScheduledTask:
    """创建定时任务"""
    payload = task.model_dump()
    payload["task_type"] = "salt"
    db_task = ScheduledTask(
        **payload,
        created_by=created_by,
    )
    
    # 计算下次执行时间
    try:
        from croniter import croniter
        now = datetime.now()
        cron = croniter(db_task.cron_expression, now)
        db_task.next_run_at = cron.get_next(datetime)
    except Exception as e:
        logger.error(f"计算下次执行时间失败: {e}")
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(
    db: AsyncSession, task_id: int, task: ScheduledTaskUpdate
) -> Optional[ScheduledTask]:
    """更新定时任务"""
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task.model_dump(exclude_unset=True)
    if "task_type" in update_data:
        update_data["task_type"] = "salt"
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    # 如果更新了 Cron 表达式,重新计算下次执行时间
    if "cron_expression" in update_data:
        try:
            from croniter import croniter
            now = datetime.now()
            cron = croniter(db_task.cron_expression, now)
            db_task.next_run_at = cron.get_next(datetime)
        except Exception as e:
            logger.error(f"计算下次执行时间失败: {e}")
    
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """删除定时任务"""
    db_task = await get_task(db, task_id)
    if not db_task:
        return False
    
    await db.delete(db_task)
    await db.commit()
    return True


async def toggle_task_enabled(db: AsyncSession, task_id: int) -> Optional[ScheduledTask]:
    """切换任务启用状态"""
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    
    db_task.enabled = not db_task.enabled
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_enabled_tasks(db: AsyncSession) -> List[ScheduledTask]:
    """获取所有启用的任务"""
    result = await db.execute(
        select(ScheduledTask).where(ScheduledTask.enabled == True)
    )
    return result.scalars().all()


async def update_task_execution_time(
    db: AsyncSession, task_id: int
) -> Optional[ScheduledTask]:
    """更新任务执行时间"""
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    
    now = datetime.now()
    db_task.last_run_at = now
    
    # 计算下次执行时间
    try:
        from croniter import croniter
        cron = croniter(db_task.cron_expression, now)
        db_task.next_run_at = cron.get_next(datetime)
    except Exception as e:
        logger.error(f"计算下次执行时间失败: {e}")
    
    await db.commit()
    await db.refresh(db_task)
    return db_task
