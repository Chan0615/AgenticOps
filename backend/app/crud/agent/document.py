"""文档 CRUD"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models.agent import Document, DocumentChunk


async def get_doc_list(
    db: AsyncSession, kb_id: int, skip: int = 0, limit: int = 100
) -> List[Document]:
    result = await db.execute(
        select(Document)
        .where(Document.kb_id == kb_id)
        .offset(skip)
        .limit(limit)
        .order_by(Document.id.desc())
    )
    return result.scalars().all()


async def get_doc_by_id(db: AsyncSession, doc_id: int) -> Optional[Document]:
    result = await db.execute(select(Document).where(Document.id == doc_id))
    return result.scalar_one_or_none()


async def create_doc(db: AsyncSession, kb_id: int, data: dict) -> Document:
    data["kb_id"] = kb_id
    doc = Document(**data)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def update_doc(db: AsyncSession, doc_id: int, data: dict) -> Optional[Document]:
    doc = await get_doc_by_id(db, doc_id)
    if not doc:
        return None
    for k, v in data.items():
        if v is not None:
            setattr(doc, k, v)
    await db.commit()
    await db.refresh(doc)
    return doc


async def delete_doc(db: AsyncSession, doc_id: int) -> bool:
    doc = await get_doc_by_id(db, doc_id)
    if not doc:
        return False
    await db.delete(doc)
    await db.commit()
    return True


async def save_chunks(db: AsyncSession, doc_id: int, kb_id: int, chunks: list[str]):
    """保存文档分块"""
    # 先删旧分块
    from sqlalchemy import delete

    await db.execute(delete(DocumentChunk).where(DocumentChunk.doc_id == doc_id))

    for i, content in enumerate(chunks):
        chunk = DocumentChunk(
            doc_id=doc_id, kb_id=kb_id, chunk_index=i, content=content
        )
        db.add(chunk)

    # 更新文档分块数
    doc = await get_doc_by_id(db, doc_id)
    if doc:
        doc.chunk_count = len(chunks)

    await db.commit()


async def search_chunks(
    db: AsyncSession, kb_id: int, query: str, top_k: int = 5
) -> List[DocumentChunk]:
    """简单文本搜索（后续替换为向量搜索）"""
    result = await db.execute(
        select(DocumentChunk)
        .where(DocumentChunk.kb_id == kb_id)
        .where(DocumentChunk.content.contains(query))
        .limit(top_k)
    )
    return result.scalars().all()
