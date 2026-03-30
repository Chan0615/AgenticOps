"""
知识库文档 CRUD 操作
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from app.models.models import KnowledgeDocument, DocumentChunk


async def create_document(db: AsyncSession, doc_data: dict) -> KnowledgeDocument:
    """创建文档记录"""
    document = KnowledgeDocument(**doc_data)
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


async def get_document_by_id(db: AsyncSession, doc_id: int) -> Optional[KnowledgeDocument]:
    """根据ID获取文档"""
    result = await db.execute(
        select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id)
    )
    return result.scalar_one_or_none()


async def get_document_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[KnowledgeDocument]:
    """获取文档列表"""
    query = select(KnowledgeDocument)
    
    if status:
        query = query.where(KnowledgeDocument.status == status)
    
    if search:
        query = query.where(KnowledgeDocument.name.contains(search))
    
    query = query.order_by(desc(KnowledgeDocument.created_at))
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


async def update_document(
    db: AsyncSession,
    doc_id: int,
    update_data: dict
) -> Optional[KnowledgeDocument]:
    """更新文档信息"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(document, key, value)
    
    await db.commit()
    await db.refresh(document)
    return document


async def delete_document(db: AsyncSession, doc_id: int) -> bool:
    """删除文档"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        return False
    
    await db.delete(document)
    await db.commit()
    return True


async def create_chunks(
    db: AsyncSession,
    document_id: int,
    chunks_data: List[dict]
) -> List[DocumentChunk]:
    """批量创建分片记录"""
    chunks = []
    for chunk_data in chunks_data:
        chunk_data['document_id'] = document_id
        chunk = DocumentChunk(**chunk_data)
        db.add(chunk)
        chunks.append(chunk)
    
    await db.commit()
    for chunk in chunks:
        await db.refresh(chunk)
    
    return chunks


async def get_chunks_by_document(
    db: AsyncSession,
    document_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[DocumentChunk]:
    """获取文档的分片列表"""
    result = await db.execute(
        select(DocumentChunk)
        .where(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_chunk_by_id(
    db: AsyncSession,
    chunk_id: int
) -> Optional[DocumentChunk]:
    """根据ID获取分片"""
    result = await db.execute(
        select(DocumentChunk).where(DocumentChunk.id == chunk_id)
    )
    return result.scalar_one_or_none()
