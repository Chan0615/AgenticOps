"""智能问数对话 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.schemas.dataquery import (
    QueryAskRequest,
    QueryAskResponse,
    QueryHistoryResponse,
    QueryHistoryListResponse,
    QueryHistoryDetailResponse,
)
from app.schemas.system.user import UserResponse
from app.crud.dataquery import history as history_crud
from app.api.auth.auth import get_current_user
from app.services import dataquery_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dataquery/chat", tags=["智能问数"])


@router.post("/ask", response_model=QueryAskResponse)
async def ask_question(
    request: QueryAskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """提交自然语言问题（非流式）"""
    result = await dataquery_service.ask(
        db=db,
        user_id=current_user.id,
        datasource_id=request.datasource_id,
        question=request.question,
        conversation_history=request.conversation_history,
    )
    return result


@router.post("/ask/stream")
async def ask_question_stream(
    request: QueryAskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """提交自然语言问题（SSE 流式）"""
    return StreamingResponse(
        dataquery_service.ask_stream(
            db=db,
            user_id=current_user.id,
            datasource_id=request.datasource_id,
            question=request.question,
            conversation_history=request.conversation_history,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ============ 查询历史 ============


@router.get("/history", response_model=QueryHistoryListResponse)
async def list_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    datasource_id: Optional[int] = Query(None, description="数据源ID"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """查询历史列表"""
    skip = (page - 1) * page_size
    histories, total = await history_crud.get_query_histories(
        db, user_id=current_user.id, datasource_id=datasource_id,
        skip=skip, limit=page_size,
    )
    return QueryHistoryListResponse(
        code=200,
        message="success",
        data=[QueryHistoryResponse.model_validate(h) for h in histories],
        total=total,
    )


@router.get("/history/{history_id}", response_model=QueryHistoryDetailResponse)
async def get_history_detail(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """查询历史详情（含结果数据）"""
    history = await history_crud.get_query_history(db, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="记录不存在")
    return history


@router.delete("/history/{history_id}")
async def delete_history(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """删除查询记录"""
    success = await history_crud.delete_query_history(db, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"code": 200, "message": "删除成功"}


@router.get("/export/{history_id}")
async def export_excel(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """导出查询结果为 Excel"""
    history = await history_crud.get_query_history(db, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="记录不存在")

    excel_bytes = await dataquery_service.export_to_excel(
        db, history_id, history.datasource_id
    )
    if not excel_bytes:
        raise HTTPException(status_code=500, detail="导出失败，无数据或执行异常")

    filename = f"query_result_{history_id}.xlsx"
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
