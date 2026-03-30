"""
知识库管理 API
"""
import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.api.common.auth import get_current_user
from app.models.models import User
from app.crud.knowledge.document import (
    create_document, get_document_by_id, get_document_list,
    update_document, delete_document, get_chunks_by_document
)
from app.rag.agents import DocumentProcessor, VectorStoreManager

router = APIRouter(prefix="/knowledge", tags=["知识库"])

# 上传文件存储目录
UPLOAD_DIR = "uploads/knowledge"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的文件类型
ALLOWED_TYPES = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'doc': 'application/msword',
    'md': 'text/markdown'
}


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传文档"""
    # 检查文件类型
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型: {file_ext}，仅支持: {', '.join(ALLOWED_TYPES.keys())}"
        )
    
    # 保存文件
    file_name = f"{current_user.id}_{int(os.path.getmtime(UPLOAD_DIR))}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 创建数据库记录
    doc_data = {
        "name": name or file.filename,
        "description": description,
        "file_path": file_path,
        "file_type": file_ext,
        "file_size": os.path.getsize(file_path),
        "status": "pending",
        "created_by": current_user.id
    }
    
    document = await create_document(db, doc_data)
    
    return {
        "id": document.id,
        "name": document.name,
        "description": document.description,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "status": document.status,
        "created_at": document.created_at
    }


@router.get("/documents")
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文档列表"""
    documents = await get_document_list(db, skip=skip, limit=limit, status=status, search=search)
    
    return [
        {
            "id": doc.id,
            "name": doc.name,
            "description": doc.description,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "status": doc.status,
            "chunk_count": doc.chunk_count,
            "created_by": doc.created_by,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at
        }
        for doc in documents
    ]


@router.get("/documents/{doc_id}")
async def get_document(
    doc_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文档详情"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    return {
        "id": document.id,
        "name": document.name,
        "description": document.description,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "status": document.status,
        "chunk_count": document.chunk_count,
        "error_msg": document.error_msg,
        "created_by": document.created_by,
        "created_at": document.created_at,
        "updated_at": document.updated_at
    }


@router.put("/documents/{doc_id}")
async def update_document_info(
    doc_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新文档信息"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    update_data = {}
    if name:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    
    updated = await update_document(db, doc_id, update_data)
    
    return {
        "id": updated.id,
        "name": updated.name,
        "description": updated.description,
        "status": updated.status
    }


@router.delete("/documents/{doc_id}")
async def delete_document_api(
    doc_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除文档"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    # 删除物理文件
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # 删除数据库记录
    await delete_document(db, doc_id)
    
    return {"message": "删除成功"}


@router.post("/documents/{doc_id}/process")
async def process_document(
    doc_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """处理文档（分片并建立向量索引）"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    try:
        # 更新状态为处理中
        await update_document(db, doc_id, {"status": "processing"})
        
        # 加载文档
        processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        docs = processor.load_document(document.file_path, document.file_type)
        
        # 分片
        chunks = processor.process_documents(docs)
        
        # 保存分片到数据库
        from app.crud.knowledge.document import create_chunks
        chunks_data = [
            {
                "content": chunk.page_content,
                "chunk_index": i,
                "char_count": len(chunk.page_content)
            }
            for i, chunk in enumerate(chunks)
        ]
        await create_chunks(db, doc_id, chunks_data)
        
        # 建立向量索引
        vector_store = VectorStoreManager()
        vector_store.create_vector_store(chunks, save_path=f"vector_db/doc_{doc_id}")
        
        # 更新文档状态
        await update_document(db, doc_id, {
            "status": "indexed",
            "chunk_count": len(chunks)
        })
        
        return {
            "message": "处理成功",
            "chunk_count": len(chunks)
        }
        
    except Exception as e:
        await update_document(db, doc_id, {
            "status": "error",
            "error_msg": str(e)
        })
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.get("/documents/{doc_id}/chunks")
async def get_document_chunks(
    doc_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文档分片列表"""
    document = await get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    chunks = await get_chunks_by_document(db, doc_id, skip=skip, limit=limit)
    
    return [
        {
            "id": chunk.id,
            "chunk_index": chunk.chunk_index,
            "content": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
            "char_count": chunk.char_count,
            "faiss_id": chunk.faiss_id,
            "created_at": chunk.created_at
        }
        for chunk in chunks
    ]


@router.get("/chunks/{chunk_id}")
async def get_chunk_detail(
    chunk_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取分片详情"""
    from app.crud.knowledge.document import get_chunk_by_id
    
    chunk = await get_chunk_by_id(db, chunk_id)
    if not chunk:
        raise HTTPException(status_code=404, detail="分片不存在")
    
    return {
        "id": chunk.id,
        "document_id": chunk.document_id,
        "chunk_index": chunk.chunk_index,
        "content": chunk.content,
        "char_count": chunk.char_count,
        "faiss_id": chunk.faiss_id,
        "created_at": chunk.created_at
    }
