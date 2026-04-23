"""知识库 CRUD"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from typing import Optional, List
from app.models.agent import KnowledgeBase, Document, AgentDocumentChunk


async def get_kb_list(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[KnowledgeBase]:
    result = await db.execute(
        select(KnowledgeBase)
        .offset(skip)
        .limit(limit)
        .order_by(KnowledgeBase.id.desc())
    )
    return result.scalars().all()


async def get_kb_by_id(db: AsyncSession, kb_id: int) -> Optional[KnowledgeBase]:
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    return result.scalar_one_or_none()


async def create_kb(db: AsyncSession, data: dict) -> KnowledgeBase:
    kb = KnowledgeBase(**data)
    db.add(kb)
    await db.commit()
    await db.refresh(kb)
    return kb


async def update_kb(
    db: AsyncSession, kb_id: int, data: dict
) -> Optional[KnowledgeBase]:
    kb = await get_kb_by_id(db, kb_id)
    if not kb:
        return None
    for k, v in data.items():
        if v is not None:
            setattr(kb, k, v)
    await db.commit()
    await db.refresh(kb)
    return kb


async def delete_kb(db: AsyncSession, kb_id: int) -> bool:
    kb = await get_kb_by_id(db, kb_id)
    if not kb:
        return False
    await db.delete(kb)
    await db.commit()
    return True


async def update_kb_counts(db: AsyncSession, kb_id: int):
    """更新知识库的文档数和分块数"""
    doc_count = (
        await db.execute(select(func.count(Document.id)).where(Document.kb_id == kb_id))
    ).scalar() or 0
    chunk_count = (
        await db.execute(select(func.count(AgentDocumentChunk.id)).where(AgentDocumentChunk.kb_id == kb_id))
    ).scalar() or 0
    await db.execute(
        update(KnowledgeBase)
        .where(KnowledgeBase.id == kb_id)
        .values(document_count=doc_count, chunk_count=chunk_count)
    )
    await db.commit()
