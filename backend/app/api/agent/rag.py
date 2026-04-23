"""
Agent RAG API

知识库管理 + 文档上传（支持 PDF/Word/Markdown/TXT）+ RAG 对话
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.schemas.agent import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse,
    DocumentCreate,
    DocumentResponse,
    ChatRequest,
    ConversationResponse,
)
from app.schemas.system.user import UserResponse
from app.api.auth.auth import get_current_user
from app.crud.agent import knowledge as kb_crud
from app.crud.agent import document as doc_crud
from app.crud.agent import conversation as conv_crud
from app.services.rag_agent import chat, chat_stream
from app.services import document_processor, vector_store
from app.core.log_decorator import log_operation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["Agent RAG"])

# 支持的文件类型
ALLOWED_EXTENSIONS = {"txt", "md", "pdf", "docx", "doc"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


# ============ 知识库 ============


@router.get("/knowledge-bases", response_model=List[KnowledgeBaseResponse])
async def list_kbs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取知识库列表"""
    kbs = await kb_crud.get_kb_list(db, skip, limit)
    return [KnowledgeBaseResponse.model_validate(k) for k in kbs]


@router.post("/knowledge-bases", response_model=KnowledgeBaseResponse, status_code=201)
@log_operation(module="知识库管理", action="创建知识库", description="创建新知识库")
async def create_kb(
    data: KnowledgeBaseCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建知识库"""
    kb = await kb_crud.create_kb(db, data.model_dump())
    return KnowledgeBaseResponse.model_validate(kb)


@router.get("/knowledge-bases/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_kb(
    kb_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取知识库详情"""
    kb = await kb_crud.get_kb_by_id(db, kb_id)
    if not kb:
        raise HTTPException(404, "知识库不存在")
    return KnowledgeBaseResponse.model_validate(kb)


@router.put("/knowledge-bases/{kb_id}", response_model=KnowledgeBaseResponse)
@log_operation(module="知识库管理", action="更新知识库", description="更新知识库信息")
async def update_kb(
    kb_id: int,
    data: KnowledgeBaseUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新知识库"""
    kb = await kb_crud.update_kb(db, kb_id, data.model_dump(exclude_unset=True))
    if not kb:
        raise HTTPException(404, "知识库不存在")
    return KnowledgeBaseResponse.model_validate(kb)


@router.delete("/knowledge-bases/{kb_id}")
@log_operation(module="知识库管理", action="删除知识库", description="删除知识库及所有文档")
async def delete_kb(
    kb_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除知识库（同时删除 pgvector 中的向量）"""
    if not await kb_crud.delete_kb(db, kb_id):
        raise HTTPException(404, "知识库不存在")
    # 删除向量数据
    try:
        await vector_store.delete_kb_embeddings(kb_id)
    except Exception as e:
        logger.warning(f"删除向量数据失败: {e}")
    return {"message": "删除成功"}


@router.get("/knowledge-bases/{kb_id}/stats")
async def get_kb_stats(
    kb_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取知识库统计（含向量状态）"""
    kb = await kb_crud.get_kb_by_id(db, kb_id)
    if not kb:
        raise HTTPException(404, "知识库不存在")

    try:
        emb_stats = await vector_store.get_kb_embedding_stats(kb_id)
    except Exception:
        emb_stats = {"chunk_count": 0, "doc_count": 0}

    return {
        "kb_id": kb_id,
        "name": kb.name,
        "document_count": kb.document_count,
        "chunk_count": kb.chunk_count,
        "indexed_chunks": emb_stats["chunk_count"],
        "indexed_docs": emb_stats["doc_count"],
    }


# ============ 文档 ============


@router.get("/knowledge-bases/{kb_id}/documents", response_model=List[DocumentResponse])
async def list_docs(
    kb_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取知识库的文档列表"""
    docs = await doc_crud.get_doc_list(db, kb_id, skip, limit)
    return [DocumentResponse.model_validate(d) for d in docs]


@router.post(
    "/knowledge-bases/{kb_id}/documents",
    response_model=DocumentResponse,
    status_code=201,
)
@log_operation(module="知识库管理", action="添加文档", description="通过文本添加文档")
async def create_doc(
    kb_id: int,
    data: DocumentCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """通过文本内容添加文档"""
    # 创建文档记录
    doc = await doc_crud.create_doc(db, kb_id, data.model_dump())

    # 分块
    chunks = document_processor.process_text(data.content, source=data.title)
    await doc_crud.save_chunks(db, doc.id, kb_id, [c["content"] for c in chunks])
    await kb_crud.update_kb_counts(db, kb_id)

    # 生成嵌入并存储到 pgvector
    try:
        texts = [c["content"] for c in chunks]
        embeddings = await vector_store.generate_embeddings(texts)
        for i, c in enumerate(chunks):
            c["embedding"] = embeddings[i]
        await vector_store.store_embeddings(kb_id, doc.id, chunks)
    except Exception as e:
        logger.error(f"向量索引失败: {e}", exc_info=True)
        # 不影响文档保存，后续可以重新索引

    # 刷新文档状态
    await db.refresh(doc)
    return DocumentResponse.model_validate(doc)


@router.post("/knowledge-bases/{kb_id}/upload")
@log_operation(module="知识库管理", action="上传文档", description="上传文件到知识库")
async def upload_document(
    kb_id: int,
    file: UploadFile = File(...),
    use_llm_split: bool = Form(True),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    上传文件到知识库

    支持格式：PDF、Word(.docx)、Markdown(.md)、文本(.txt)
    """
    # 验证知识库存在
    kb = await kb_crud.get_kb_by_id(db, kb_id)
    if not kb:
        raise HTTPException(404, "知识库不存在")

    # 验证文件类型
    filename = file.filename or "unknown.txt"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400,
            f"不支持的文件类型: .{ext}，支持: {', '.join('.' + e for e in ALLOWED_EXTENSIONS)}"
        )

    # 读取文件
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(400, f"文件大小超过限制（最大 {MAX_FILE_SIZE // 1024 // 1024}MB）")

    if not file_bytes:
        raise HTTPException(400, "文件内容为空")

    # 处理文档：解析 → 清洗 → 分割
    try:
        chunks = await document_processor.process_document(
            file_bytes=file_bytes,
            filename=filename,
            use_llm_split=use_llm_split,
        )
    except Exception as e:
        raise HTTPException(400, f"文件处理失败: {str(e)}")

    if not chunks:
        raise HTTPException(400, "文件内容为空或无法解析")

    # 提取全文（用于存储到 MySQL document 表）
    full_text = "\n\n".join(c["content"] for c in chunks)

    # 创建文档记录（MySQL）
    doc = await doc_crud.create_doc(db, kb_id, {
        "title": filename,
        "content": full_text[:50000],  # 截断保存
        "source": filename,
        "doc_type": ext,
    })

    # 保存分块到 MySQL
    await doc_crud.save_chunks(db, doc.id, kb_id, [c["content"] for c in chunks])
    await kb_crud.update_kb_counts(db, kb_id)

    # 生成嵌入向量并存储到 pgvector
    indexed_count = 0
    try:
        texts = [c["content"] for c in chunks]
        embeddings = await vector_store.generate_embeddings(texts)
        for i, c in enumerate(chunks):
            c["embedding"] = embeddings[i]
        indexed_count = await vector_store.store_embeddings(kb_id, doc.id, chunks)
    except Exception as e:
        logger.error(f"向量索引失败: {e}", exc_info=True)

    await db.refresh(doc)

    return {
        "message": "上传成功",
        "document": DocumentResponse.model_validate(doc),
        "chunks": len(chunks),
        "indexed": indexed_count,
    }


@router.get("/documents/{doc_id}/chunks")
async def get_doc_chunks(
    doc_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取文档的分块列表"""
    from sqlalchemy import select
    from app.models.agent import AgentDocumentChunk

    doc = await doc_crud.get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(404, "文档不存在")

    result = await db.execute(
        select(AgentDocumentChunk)
        .where(AgentDocumentChunk.doc_id == doc_id)
        .order_by(AgentDocumentChunk.chunk_index)
    )
    chunks = result.scalars().all()

    return {
        "doc_id": doc_id,
        "doc_title": doc.title,
        "total": len(chunks),
        "chunks": [
            {
                "id": c.id,
                "chunk_index": c.chunk_index,
                "content": c.content,
                "char_count": len(c.content),
            }
            for c in chunks
        ],
    }


@router.delete("/documents/{doc_id}")
@log_operation(module="知识库管理", action="删除文档", description="删除文档")
async def delete_doc(
    doc_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除文档（同时删除向量）"""
    doc = await doc_crud.get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(404, "文档不存在")
    kb_id = doc.kb_id

    # 删除向量
    try:
        await vector_store.delete_doc_embeddings(kb_id, doc_id)
    except Exception as e:
        logger.warning(f"删除向量数据失败: {e}")

    await doc_crud.delete_doc(db, doc_id)
    await kb_crud.update_kb_counts(db, kb_id)
    return {"message": "删除成功"}


@router.post("/documents/{doc_id}/reindex")
async def reindex_document(
    doc_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """重新索引文档（重新生成嵌入向量）"""
    doc = await doc_crud.get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(404, "文档不存在")

    # 获取分块
    from sqlalchemy import select
    from app.models.agent import AgentDocumentChunk

    result = await db.execute(
        select(AgentDocumentChunk)
        .where(AgentDocumentChunk.doc_id == doc_id)
        .order_by(AgentDocumentChunk.chunk_index)
    )
    db_chunks = result.scalars().all()

    if not db_chunks:
        raise HTTPException(400, "文档没有分块数据")

    # 生成嵌入
    texts = [c.content for c in db_chunks]
    embeddings = await vector_store.generate_embeddings(texts)

    chunks = []
    for i, c in enumerate(db_chunks):
        chunks.append({
            "content": c.content,
            "embedding": embeddings[i],
            "chunk_index": c.chunk_index,
            "metadata": {"source": doc.title or doc.source or ""},
        })

    indexed = await vector_store.store_embeddings(doc.kb_id, doc_id, chunks)

    return {"message": "重新索引完成", "indexed": indexed}


# ============ 对话 ============


@router.post("/chat")
@log_operation(module="AI对话", action="发起对话", description="RAG 知识库问答")
async def chat_endpoint(
    req: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """RAG 对话（非流式）"""
    result = await chat(
        db=db,
        user_id=current_user.id,
        message=req.message,
        kb_id=req.kb_id,
        conversation_id=req.conversation_id,
    )
    return result


@router.post("/chat/stream")
async def chat_stream_endpoint(
    req: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """RAG 对话（SSE 流式）"""
    return StreamingResponse(
        chat_stream(
            db=db,
            user_id=current_user.id,
            message=req.message,
            kb_id=req.kb_id,
            conversation_id=req.conversation_id,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ============ 对话管理 ============


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    kb_id: Optional[int] = Query(None, description="按知识库筛选"),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取对话列表"""
    convs = await conv_crud.get_conversations(db, current_user.id)
    if kb_id is not None:
        convs = [c for c in convs if c.kb_id == kb_id]
    return [ConversationResponse.model_validate(c) for c in convs]


@router.get("/conversations/{conv_id}", response_model=ConversationResponse)
async def get_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取对话详情（含消息历史）"""
    conv = await conv_crud.get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(404, "对话不存在")
    return ConversationResponse.model_validate(conv)


@router.delete("/conversations/{conv_id}")
@log_operation(module="AI对话", action="删除对话", description="删除对话记录")
async def delete_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除对话"""
    if not await conv_crud.delete_conversation(db, conv_id):
        raise HTTPException(404, "对话不存在")
    return {"message": "删除成功"}
