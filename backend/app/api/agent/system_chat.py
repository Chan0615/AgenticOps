"""
系统 AI 助手 API 路由

提供带 tool-calling 能力的系统 AI 对话接口：
  POST /api/assistant/chat         - 普通对话
  POST /api/assistant/chat/stream  - SSE 流式对话
  POST /api/assistant/confirm      - 用户确认写操作
  GET  /api/assistant/conversations        - 对话列表
  GET  /api/assistant/conversations/{id}   - 对话详情
  DELETE /api/assistant/conversations/{id} - 删除对话
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.api.auth.auth import get_current_user
from app.schemas.system.user import UserResponse
from app.schemas.assistant_agent import (
    ChatRequest,
    ChatResponse,
    ConfirmRequest,
    ConfirmResponse,
    ConversationItem,
    PendingAction,
)
from app.services.system_agent import (
    system_chat,
    system_chat_stream,
    system_confirm_action,
)
from app.crud.agent import conversation as conv_crud
from app.core.log_decorator import log_operation

router = APIRouter(prefix="/assistant", tags=["系统 AI 助手"])


@router.post("/chat", response_model=ChatResponse)
@log_operation(module="系统AI助手", action="发起对话", description="系统 AI 智能对话")
async def chat_endpoint(
    req: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await system_chat(
        db=db,
        user_id=current_user.id,
        message=req.message,
        conversation_id=req.conversation_id,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return ChatResponse(
        conversation_id=result["conversation_id"],
        answer=result["answer"],
        pending_action=(
            PendingAction(**result["pending_action"])
            if result.get("pending_action")
            else None
        ),
        sources=result.get("sources", []),
    )


@router.post("/chat/stream")
async def chat_stream_endpoint(
    req: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return StreamingResponse(
        system_chat_stream(
            db=db,
            user_id=current_user.id,
            message=req.message,
            conversation_id=req.conversation_id,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/confirm", response_model=ConfirmResponse)
@log_operation(
    module="系统AI助手", action="确认执行操作", description="用户确认 AI 写操作后执行"
)
async def confirm_action_endpoint(
    req: ConfirmRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await system_confirm_action(
        db=db,
        user_id=current_user.id,
        tool_name=req.tool_name,
        tool_args=req.tool_args,
        conversation_id=req.conversation_id,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return ConfirmResponse(
        conversation_id=result["conversation_id"],
        answer=result["answer"],
        success=result["success"],
    )


@router.get("/conversations", response_model=List[ConversationItem])
async def list_conversations(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户的系统助手对话列表（kb_id=None 的对话）"""
    convs = await conv_crud.get_conversations(db, current_user.id)
    sys_convs = [c for c in convs if c.kb_id is None]
    return [ConversationItem.model_validate(c) for c in sys_convs]


@router.get("/conversations/{conv_id}")
async def get_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv = await conv_crud.get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此对话")

    messages = []
    for msg in conv.messages or []:
        messages.append(
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "sources": msg.sources,
                "created_at": (
                    msg.created_at.isoformat() if msg.created_at else None
                ),
            }
        )

    return {
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
        "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
        "messages": messages,
    }


@router.delete("/conversations/{conv_id}")
@log_operation(module="系统AI助手", action="删除对话", description="删除系统 AI 对话记录")
async def delete_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv = await conv_crud.get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此对话")

    await conv_crud.delete_conversation(db, conv_id)
    return {"message": "删除成功"}
