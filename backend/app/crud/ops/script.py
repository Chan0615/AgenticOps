"""脚本 CRUD 操作"""

from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops import Script
from app.schemas.script import ScriptCreate, ScriptUpdate
import logging

logger = logging.getLogger(__name__)


async def get_script(db: AsyncSession, script_id: int) -> Optional[Script]:
    """根据ID获取脚本"""
    result = await db.execute(select(Script).where(Script.id == script_id))
    return result.scalar_one_or_none()


async def get_scripts(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = None,
    script_type: Optional[str] = None,
) -> tuple[List[Script], int]:
    """获取脚本列表"""
    query = select(Script)
    count_query = select(func.count(Script.id))
    
    if name:
        query = query.where(Script.name.ilike(f"%{name}%"))
        count_query = count_query.where(Script.name.ilike(f"%{name}%"))
    
    if script_type:
        query = query.where(Script.script_type == script_type)
        count_query = count_query.where(Script.script_type == script_type)
    
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
    db_script = Script(
        **payload,
        content=file_path,
        created_by=created_by,
    )
    db.add(db_script)
    await db.commit()
    await db.refresh(db_script)
    return db_script


async def update_script(db: AsyncSession, script_id: int, script: ScriptUpdate) -> Optional[Script]:
    """更新脚本"""
    db_script = await get_script(db, script_id)
    if not db_script:
        return None
    
    update_data = script.model_dump(exclude_unset=True)
    if "file_path" in update_data:
        update_data["content"] = update_data.pop("file_path")
    for field, value in update_data.items():
        setattr(db_script, field, value)
    
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
