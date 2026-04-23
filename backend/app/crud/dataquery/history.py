"""查询历史 CRUD 操作"""

from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dataquery import QueryHistory
import logging

logger = logging.getLogger(__name__)


async def create_query_history(
    db: AsyncSession,
    datasource_id: int,
    user_id: int,
    question: str,
    generated_sql: Optional[str] = None,
    result_summary: Optional[str] = None,
    result_data: Optional[list] = None,
    row_count: int = 0,
    execution_time: Optional[float] = None,
    status: str = "success",
    error_message: Optional[str] = None,
    chart_type: Optional[str] = None,
    chart_config: Optional[dict] = None,
) -> QueryHistory:
    """创建查询历史记录"""
    history = QueryHistory(
        datasource_id=datasource_id,
        user_id=user_id,
        question=question,
        generated_sql=generated_sql,
        result_summary=result_summary,
        result_data=result_data,
        row_count=row_count,
        execution_time=execution_time,
        status=status,
        error_message=error_message,
        chart_type=chart_type,
        chart_config=chart_config,
    )
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_query_history(db: AsyncSession, history_id: int) -> Optional[QueryHistory]:
    """获取单条查询历史"""
    result = await db.execute(
        select(QueryHistory).where(QueryHistory.id == history_id)
    )
    return result.scalar_one_or_none()


async def get_query_histories(
    db: AsyncSession,
    user_id: int,
    datasource_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
) -> tuple[List[QueryHistory], int]:
    """获取查询历史列表"""
    query = select(QueryHistory).where(QueryHistory.user_id == user_id)
    count_query = select(func.count(QueryHistory.id)).where(
        QueryHistory.user_id == user_id
    )

    if datasource_id:
        query = query.where(QueryHistory.datasource_id == datasource_id)
        count_query = count_query.where(QueryHistory.datasource_id == datasource_id)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset(skip).limit(limit).order_by(QueryHistory.created_at.desc())
    result = await db.execute(query)
    histories = result.scalars().all()

    return histories, total


async def delete_query_history(db: AsyncSession, history_id: int) -> bool:
    """删除查询历史"""
    history = await get_query_history(db, history_id)
    if not history:
        return False
    await db.delete(history)
    await db.commit()
    return True
