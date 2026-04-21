"""
运维 AI 助手 API 路由

提供基于 Function Calling 的运维智能对话接口：
  POST /api/ops/ai/chat         - 普通对话
  POST /api/ops/ai/chat/stream  - SSE 流式对话
  POST /api/ops/ai/confirm      - 用户确认写操作
  GET  /api/ops/ai/conversations        - 对话列表
  GET  /api/ops/ai/conversations/{id}   - 对话详情
  DELETE /api/ops/ai/conversations/{id} - 删除对话
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.api.auth.auth import get_current_user
from app.schemas.system.user import UserResponse
from app.schemas.ops_agent import (
    OpsChatRequest,
    OpsChatResponse,
    OpsConfirmRequest,
    OpsConfirmResponse,
    OpsConversationItem,
    PendingAction,
)
from app.services.ops_agent import (
    ops_chat,
    ops_chat_stream,
    ops_confirm_action,
)
from app.crud.agent import conversation as conv_crud
from app.core.log_decorator import log_operation
from typing import List

router = APIRouter(prefix="/api/ops/ai", tags=["运维 AI 助手"])


@router.post("/chat", response_model=OpsChatResponse)
@log_operation(module="运维AI助手", action="发起对话", description="运维 AI 智能对话")
async def chat_endpoint(
    req: OpsChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    运维 AI 对话（非流式）

    - 只读操作（查询服务器、日志等）：AI 自主完成并返回结果
    - 写操作（执行脚本、创建任务等）：返回 pending_action，前端弹确认框
    """
    result = await ops_chat(
        db=db,
        user_id=current_user.id,
        message=req.message,
        conversation_id=req.conversation_id,
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return OpsChatResponse(
        conversation_id=result["conversation_id"],
        answer=result["answer"],
        pending_action=PendingAction(**result["pending_action"]) if result.get("pending_action") else None,
        sources=result.get("sources", []),
    )


@router.post("/chat/stream")
async def chat_stream_endpoint(
    req: OpsChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    运维 AI 对话（SSE 流式）

    SSE 事件格式：
    - `data: <text>` — 普通文本块，逐字流式输出
    - `data: [TOOL_CALL]<tool_name>` — AI 正在调用工具（前端可显示加载状态）
    - `data: [PENDING_ACTION]<json>` — 写操作待确认（前端弹出确认框）
    - `data: [DONE]` — 流结束
    """
    return StreamingResponse(
        ops_chat_stream(
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


@router.post("/confirm", response_model=OpsConfirmResponse)
@log_operation(module="运维AI助手", action="确认执行操作", description="用户确认 AI 写操作后执行")
async def confirm_action_endpoint(
    req: OpsConfirmRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    用户确认写操作后真正执行

    前端收到 pending_action 并用户点击「确认」后调用此接口。
    后端根据 tool_name 和 tool_args 执行对应的写操作工具，
    并将执行结果追加到对话历史中。
    """
    result = await ops_confirm_action(
        db=db,
        user_id=current_user.id,
        tool_name=req.tool_name,
        tool_args=req.tool_args,
        conversation_id=req.conversation_id,
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return OpsConfirmResponse(
        conversation_id=result["conversation_id"],
        answer=result["answer"],
        success=result["success"],
    )


@router.get("/conversations", response_model=List[OpsConversationItem])
async def list_conversations(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户的运维 AI 对话列表（不含知识库对话）"""
    # 获取所有对话，过滤 kb_id=None 的（即运维 AI 对话，非知识库对话）
    convs = await conv_crud.get_conversations(db, current_user.id)
    ops_convs = [c for c in convs if c.kb_id is None]
    return [OpsConversationItem.model_validate(c) for c in ops_convs]


@router.get("/conversations/{conv_id}")
async def get_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取对话详情（含消息历史）"""
    conv = await conv_crud.get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此对话")

    messages = []
    for msg in (conv.messages or []):
        messages.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "sources": msg.sources,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        })

    return {
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
        "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
        "messages": messages,
    }


@router.delete("/conversations/{conv_id}")
@log_operation(module="运维AI助手", action="删除对话", description="删除运维 AI 对话记录")
async def delete_conversation(
    conv_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除对话"""
    conv = await conv_crud.get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此对话")

    await conv_crud.delete_conversation(db, conv_id)
    return {"message": "删除成功"}
