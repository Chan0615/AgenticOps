"""Agent RAG API"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.agent import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse,
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    ChatRequest,
    ConversationResponse,
    MessageResponse,
)
from app.schemas.system.user import UserResponse
from app.api.auth.auth import get_current_user
from app.crud.agent import knowledge as kb_crud
from app.crud.agent import document as doc_crud
from app.crud.agent import conversation as conv_crud
from app.services.rag_agent import chat, chat_stream

router = APIRouter(prefix="/agent", tags=["Agent RAG"])


# ============ 知识库 ============
@router.get("/knowledge-bases", response_model=List[KnowledgeBaseResponse])
async def list_kbs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kbs = await kb_crud.get_kb_list(db, skip, limit)
    return [KnowledgeBaseResponse.model_validate(k) for k in kbs]


@router.post("/knowledge-bases", response_model=KnowledgeBaseResponse, status_code=201)
async def create_kb(
    data: KnowledgeBaseCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kb = await kb_crud.create_kb(db, data.model_dump())
    return KnowledgeBaseResponse.model_validate(kb)


@router.get("/knowledge-bases/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_kb(
    kb_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kb = await kb_crud.get_kb_by_id(db, kb_id)
    if not kb:
        raise HTTPException(404, "知识库不存在")
    return KnowledgeBaseResponse.model_validate(kb)


@router.put("/knowledge-bases/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_kb(
    kb_id: int,
    data: KnowledgeBaseUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kb = await kb_crud.update_kb(db, kb_id, data.model_dump(exclude_unset=True))
    if not kb:
        raise HTTPException(404, "知识库不存在")
    return KnowledgeBaseResponse.model_validate(kb)


@router.delete("/knowledge-bases/{kb_id}")
async def delete_kb(
    kb_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not await kb_crud.delete_kb(db, kb_id):
        raise HTTPException(404, "知识库不存在")
    return {"message": "删除成功"}


# ============ 文档 ============
@router.get("/knowledge-bases/{kb_id}/documents", response_model=List[DocumentResponse])
async def list_docs(
    kb_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    docs = await doc_crud.get_doc_list(db, kb_id, skip, limit)
    return [DocumentResponse.model_validate(d) for d in docs]


@router.post(
    "/knowledge-bases/{kb_id}/documents",
    response_model=DocumentResponse,
    status_code=201,
)
async def create_doc(
    kb_id: int,
    data: DocumentCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    doc = await doc_crud.create_doc(db, kb_id, data.model_dump())
    # 简单分块（每 500 字一块）
    content = data.content
    chunks = [content[i : i + 500] for i in range(0, len(content), 500)]
    await doc_crud.save_chunks(db, doc.id, kb_id, chunks)
    await kb_crud.update_kb_counts(db, kb_id)
    return DocumentResponse.model_validate(doc)


@router.delete("/documents/{doc_id}")
async def delete_doc(
    doc_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    doc = await doc_crud.get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(404, "文档不存在")
    kb_id = doc.kb_id
    await doc_crud.delete_doc(db, doc_id)
    await kb_crud.update_kb_counts(db, kb_id)
    return {"message": "删除成功"}


# ============ 对话 ============
@router.post("/chat")
async def chat_endpoint(
    req: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
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
    async def event_generator():
        async for char in chat_stream(
            db=db,
            user_id=current_user.id,
            message=req.message,
            kb_id=req.kb_id,
            conversation_id=req.conversation_id,
        ):
            yield f"data: {char}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    convs = await conv_crud.get_conversations(db, current_user.id)
    return [ConversationResponse.model_validate(c) for c in convs]


@router.get("/conversations/{conv_id}", response_model=ConversationResponse)
async def get_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv = await conv_crud.get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(404, "对话不存在")
    return ConversationResponse.model_validate(conv)


@router.delete("/conversations/{conv_id}")
async def delete_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not await conv_crud.delete_conversation(db, conv_id):
        raise HTTPException(404, "对话不存在")
    return {"message": "删除成功"}
