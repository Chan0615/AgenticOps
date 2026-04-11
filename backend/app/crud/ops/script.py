"""脚本 CRUD 操作"""

from typing import List, Optional
from pathlib import Path
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops import OpsGroup, OpsScriptVersion, Script
from app.schemas.script import ScriptCreate, ScriptUpdate
import logging

logger = logging.getLogger(__name__)


async def _append_script_version(
    db: AsyncSession,
    script_id: int,
    file_path: str,
    source_file_name: Optional[str] = None,
    note: Optional[str] = None,
    created_by: Optional[str] = None,
) -> OpsScriptVersion:
    next_no_result = await db.execute(
        select(func.coalesce(func.max(OpsScriptVersion.version_no), 0) + 1).where(
            OpsScriptVersion.script_id == script_id
        )
    )
    next_version_no = int(next_no_result.scalar() or 1)

    db_version = OpsScriptVersion(
        script_id=script_id,
        version_no=next_version_no,
        file_path=file_path,
        source_file_name=source_file_name or Path(file_path).name,
        note=note,
        created_by=created_by,
    )
    db.add(db_version)
    await db.flush()
    return db_version


async def get_script(db: AsyncSession, script_id: int) -> Optional[Script]:
    """根据ID获取脚本"""
    result = await db.execute(
        select(Script)
        .options(joinedload(Script.project), joinedload(Script.group))
        .where(Script.id == script_id)
    )
    return result.scalar_one_or_none()


async def get_scripts(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = None,
    script_type: Optional[str] = None,
    project_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> tuple[List[Script], int]:
    """获取脚本列表"""
    query = select(Script).options(joinedload(Script.project), joinedload(Script.group))
    count_query = select(func.count(Script.id))
    
    if name:
        query = query.where(Script.name.ilike(f"%{name}%"))
        count_query = count_query.where(Script.name.ilike(f"%{name}%"))
    
    if script_type:
        query = query.where(Script.script_type == script_type)
        count_query = count_query.where(Script.script_type == script_type)

    if project_id is not None:
        query = query.where(Script.project_id == project_id)
        count_query = count_query.where(Script.project_id == project_id)

    if group_id is not None:
        query = query.where(Script.group_id == group_id)
        count_query = count_query.where(Script.group_id == group_id)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset(skip).limit(limit).order_by(Script.created_at.desc())
    result = await db.execute(query)
    scripts = result.scalars().all()
    
    return scripts, total


async def create_script(db: AsyncSession, script: ScriptCreate, created_by: str = None) -> Script:
    """创建脚本"""
    payload = script.model_dump()
    file_path = payload.pop("file_path")
    group_id = payload.get("group_id")
    if group_id:
        group_result = await db.execute(select(OpsGroup).where(OpsGroup.id == group_id))
        group = group_result.scalar_one_or_none()
        if not group:
            raise ValueError("所属分组不存在")
        payload["project_id"] = group.project_id
    db_script = Script(
        **payload,
        content=file_path,
        created_by=created_by,
    )
    db.add(db_script)
    await db.flush()
    await _append_script_version(
        db,
        script_id=db_script.id,
        file_path=file_path,
        source_file_name=Path(file_path).name,
        note="初始版本",
        created_by=created_by,
    )
    await db.commit()
    await db.refresh(db_script)
    return db_script


async def update_script(
    db: AsyncSession,
    script_id: int,
    script: ScriptUpdate,
    updated_by: Optional[str] = None,
) -> Optional[Script]:
    """更新脚本"""
    db_script = await get_script(db, script_id)
    if not db_script:
        return None
    
    update_data = script.model_dump(exclude_unset=True)
    new_file_path = None
    if "file_path" in update_data:
        new_file_path = update_data.pop("file_path")
        update_data["content"] = new_file_path
    if "group_id" in update_data and update_data["group_id"]:
        group_result = await db.execute(select(OpsGroup).where(OpsGroup.id == update_data["group_id"]))
        group = group_result.scalar_one_or_none()
        if not group:
            raise ValueError("所属分组不存在")
        update_data["project_id"] = group.project_id
    for field, value in update_data.items():
        setattr(db_script, field, value)

    if new_file_path:
        await _append_script_version(
            db,
            script_id=db_script.id,
            file_path=new_file_path,
            source_file_name=Path(new_file_path).name,
            note="替换脚本文件",
            created_by=updated_by or db_script.created_by,
        )

    await db.commit()
    await db.refresh(db_script)
    return db_script


async def get_script_version(db: AsyncSession, script_id: int, version_id: int) -> Optional[OpsScriptVersion]:
    result = await db.execute(
        select(OpsScriptVersion).where(
            OpsScriptVersion.id == version_id,
            OpsScriptVersion.script_id == script_id,
        )
    )
    return result.scalar_one_or_none()


async def list_script_versions(db: AsyncSession, script_id: int) -> List[OpsScriptVersion]:
    result = await db.execute(
        select(OpsScriptVersion)
        .where(OpsScriptVersion.script_id == script_id)
        .order_by(OpsScriptVersion.version_no.desc())
    )
    return result.scalars().all()


async def rollback_script_to_file(
    db: AsyncSession,
    script_id: int,
    file_path: str,
    source_file_name: Optional[str],
    note: Optional[str],
    updated_by: Optional[str],
    script_type: Optional[str] = None,
) -> Optional[Script]:
    db_script = await get_script(db, script_id)
    if not db_script:
        return None

    db_script.content = file_path
    if script_type:
        db_script.script_type = script_type
    await _append_script_version(
        db,
        script_id=script_id,
        file_path=file_path,
        source_file_name=source_file_name or Path(file_path).name,
        note=note or "回滚版本",
        created_by=updated_by,
    )
    await db.commit()
    await db.refresh(db_script)
    return db_script


async def delete_script(db: AsyncSession, script_id: int) -> bool:
    """删除脚本"""
    db_script = await get_script(db, script_id)
    if not db_script:
        return False
    
    await db.delete(db_script)
    await db.commit()
    return True
