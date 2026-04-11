"""项目与分组 CRUD 操作"""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ops import OpsGroup, OpsProject, ScheduledTask, Script
from app.schemas.group import (
    OpsGroupCreate,
    OpsGroupUpdate,
    OpsProjectCreate,
    OpsProjectUpdate,
)


def _normalize_text(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def _is_protected_project(project: OpsProject) -> bool:
    code = _normalize_text(project.code)
    name = _normalize_text(project.name)
    creator = _normalize_text(project.created_by)
    return code == "default" or name == "default" or "默认" in name or creator == "system"


def _is_protected_group(group: OpsGroup) -> bool:
    name = _normalize_text(group.name)
    creator = _normalize_text(group.created_by)
    return name == "default" or "默认" in name or creator == "system"


async def get_project(db: AsyncSession, project_id: int) -> Optional[OpsProject]:
    result = await db.execute(select(OpsProject).where(OpsProject.id == project_id))
    return result.scalar_one_or_none()


async def get_projects(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = None,
) -> tuple[List[OpsProject], int]:
    query = select(OpsProject)
    count_query = select(func.count(OpsProject.id))

    if name:
        query = query.where(OpsProject.name.ilike(f"%{name}%"))
        count_query = count_query.where(OpsProject.name.ilike(f"%{name}%"))

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset(skip).limit(limit).order_by(OpsProject.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all(), total


async def create_project(
    db: AsyncSession,
    project: OpsProjectCreate,
    created_by: Optional[str] = None,
) -> OpsProject:
    db_project = OpsProject(**project.model_dump(), created_by=created_by)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def update_project(
    db: AsyncSession,
    project_id: int,
    project: OpsProjectUpdate,
) -> Optional[OpsProject]:
    db_project = await get_project(db, project_id)
    if not db_project:
        return None

    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    await db.commit()
    await db.refresh(db_project)
    return db_project


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    db_project = await get_project(db, project_id)
    if not db_project:
        return False

    if _is_protected_project(db_project):
        raise PermissionError("系统默认项目不允许删除")

    group_count_result = await db.execute(
        select(func.count(OpsGroup.id)).where(OpsGroup.project_id == project_id)
    )
    script_count_result = await db.execute(
        select(func.count(Script.id)).where(Script.project_id == project_id)
    )
    task_count_result = await db.execute(
        select(func.count(ScheduledTask.id)).where(ScheduledTask.project_id == project_id)
    )
    has_refs = (
        (group_count_result.scalar() or 0) > 0
        or (script_count_result.scalar() or 0) > 0
        or (task_count_result.scalar() or 0) > 0
    )
    if has_refs:
        raise ValueError("项目下存在分组/脚本/任务，请先迁移或删除后再操作")

    await db.delete(db_project)
    await db.commit()
    return True


async def get_group(db: AsyncSession, group_id: int) -> Optional[OpsGroup]:
    result = await db.execute(select(OpsGroup).where(OpsGroup.id == group_id))
    return result.scalar_one_or_none()


async def get_groups(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    project_id: Optional[int] = None,
    name: Optional[str] = None,
) -> tuple[List[OpsGroup], int]:
    query = select(OpsGroup).options(joinedload(OpsGroup.project)).join(OpsProject, OpsGroup.project_id == OpsProject.id)
    count_query = select(func.count(OpsGroup.id)).select_from(OpsGroup)

    if project_id is not None:
        query = query.where(OpsGroup.project_id == project_id)
        count_query = count_query.where(OpsGroup.project_id == project_id)

    if name:
        query = query.where(OpsGroup.name.ilike(f"%{name}%"))
        count_query = count_query.where(OpsGroup.name.ilike(f"%{name}%"))

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset(skip).limit(limit).order_by(OpsGroup.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all(), total


async def create_group(
    db: AsyncSession,
    group: OpsGroupCreate,
    created_by: Optional[str] = None,
) -> OpsGroup:
    project = await get_project(db, group.project_id)
    if not project:
        raise ValueError("所属项目不存在")

    db_group = OpsGroup(**group.model_dump(), created_by=created_by)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group


async def update_group(
    db: AsyncSession,
    group_id: int,
    group: OpsGroupUpdate,
) -> Optional[OpsGroup]:
    db_group = await get_group(db, group_id)
    if not db_group:
        return None

    update_data = group.model_dump(exclude_unset=True)
    if "project_id" in update_data:
        project = await get_project(db, update_data["project_id"])
        if not project:
            raise ValueError("所属项目不存在")

    for field, value in update_data.items():
        setattr(db_group, field, value)

    await db.commit()
    await db.refresh(db_group)
    return db_group


async def delete_group(db: AsyncSession, group_id: int) -> bool:
    db_group = await get_group(db, group_id)
    if not db_group:
        return False

    if _is_protected_group(db_group):
        raise PermissionError("系统默认分组不允许删除")

    script_count_result = await db.execute(
        select(func.count(Script.id)).where(Script.group_id == group_id)
    )
    task_count_result = await db.execute(
        select(func.count(ScheduledTask.id)).where(ScheduledTask.group_id == group_id)
    )
    has_refs = (script_count_result.scalar() or 0) > 0 or (task_count_result.scalar() or 0) > 0
    if has_refs:
        raise ValueError("分组下存在脚本/任务，请先迁移或删除后再操作")

    await db.delete(db_group)
    await db.commit()
    return True
