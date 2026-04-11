"""仪表盘概览 API"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.api.auth.auth import get_current_user
from app.db.database import get_db
from app.models.agent import AgentDocumentChunk, Conversation, Document, KnowledgeBase
from app.models.models import User
from app.models.ops import OpsGroup, OpsProject, ScheduledTask, Server, TaskExecutionLog
from app.schemas.system.user import UserResponse


router = APIRouter(prefix="/api/ops/dashboard", tags=["仪表盘"])
logger = logging.getLogger(__name__)


def _relative_time(dt: datetime | None) -> str:
    if not dt:
        return "未知时间"
    delta = datetime.now() - dt
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "刚刚"
    if seconds < 3600:
        return f"{seconds // 60} 分钟前"
    if seconds < 86400:
        return f"{seconds // 3600} 小时前"
    return f"{seconds // 86400} 天前"


async def _safe_count(db: AsyncSession, stmt, fallback: int = 0) -> int:
    try:
        return (await db.execute(stmt)).scalar() or 0
    except Exception as exc:
        logger.warning("Dashboard count query failed: %s", exc)
        return fallback


@router.get("/overview")
async def get_dashboard_overview(
    project_id: int | None = Query(None, description="项目ID过滤"),
    group_id: int | None = Query(None, description="分组ID过滤"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取仪表盘概览数据。"""
    _ = current_user
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    last_24h = now - timedelta(hours=24)
    trend_days = 7
    trend_start = today_start - timedelta(days=trend_days - 1)

    project_name = None
    group_name = None
    try:
        if project_id is not None:
            project_name = (
                await db.execute(select(OpsProject.name).where(OpsProject.id == project_id))
            ).scalar_one_or_none()
        if group_id is not None:
            group_name = (
                await db.execute(select(OpsGroup.name).where(OpsGroup.id == group_id))
            ).scalar_one_or_none()
    except Exception as exc:
        logger.warning("Dashboard filter name query failed: %s", exc)

    total_users = await _safe_count(db, select(func.count(User.id)))
    active_users = await _safe_count(db, select(func.count(User.id)).where(User.status == True))

    knowledge_bases = await _safe_count(db, select(func.count(KnowledgeBase.id)))
    documents = await _safe_count(db, select(func.count(Document.id)))
    indexed_documents = await _safe_count(db, select(func.count(Document.id)).where(Document.status == True))
    chunks = await _safe_count(db, select(func.count(AgentDocumentChunk.id)))

    servers = await _safe_count(db, select(func.count(Server.id)))
    online_servers = await _safe_count(db, select(func.count(Server.id)).where(Server.status == "online"))
    offline_servers = await _safe_count(db, select(func.count(Server.id)).where(Server.status == "offline"))

    task_filters = []
    if project_id is not None:
        task_filters.append(ScheduledTask.project_id == project_id)
    if group_id is not None:
        task_filters.append(ScheduledTask.group_id == group_id)

    total_tasks = await _safe_count(db, select(func.count(ScheduledTask.id)).where(*task_filters))
    enabled_tasks = await _safe_count(
        db,
        select(func.count(ScheduledTask.id)).where(ScheduledTask.enabled == True, *task_filters),
    )

    log_filters_today = [TaskExecutionLog.created_at >= today_start]
    log_filters_last_24h = [TaskExecutionLog.created_at >= last_24h]
    log_filters_recent = []
    if project_id is not None:
        log_filters_today.append(ScheduledTask.project_id == project_id)
        log_filters_last_24h.append(ScheduledTask.project_id == project_id)
        log_filters_recent.append(ScheduledTask.project_id == project_id)
    if group_id is not None:
        log_filters_today.append(ScheduledTask.group_id == group_id)
        log_filters_last_24h.append(ScheduledTask.group_id == group_id)
        log_filters_recent.append(ScheduledTask.group_id == group_id)

    today_runs = await _safe_count(
        db,
        select(func.count(TaskExecutionLog.id))
        .select_from(TaskExecutionLog)
        .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
        .where(*log_filters_today),
    )
    failed_runs = await _safe_count(
        db,
        select(func.count(TaskExecutionLog.id))
        .select_from(TaskExecutionLog)
        .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
        .where(*log_filters_today, TaskExecutionLog.status == "failed"),
    )
    last_24h_failed_runs = await _safe_count(
        db,
        select(func.count(TaskExecutionLog.id))
        .select_from(TaskExecutionLog)
        .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
        .where(*log_filters_last_24h, TaskExecutionLog.status == "failed"),
    )

    today_chats = await _safe_count(
        db,
        select(func.count(Conversation.id)).where(Conversation.created_at >= today_start),
    )

    success_rate = (
        round(((today_runs - failed_runs) / today_runs) * 100, 1)
        if today_runs
        else 100.0
    )

    try:
        from app.api.ops.tasks import _collect_celery_health

        celery_health = _collect_celery_health()
    except Exception as exc:
        logger.warning("Dashboard celery health failed: %s", exc)
        celery_health = {
            "ok": False,
            "workers": [],
            "beat_healthy": False,
            "detail": "Celery 状态不可用",
        }

    try:
        recent_log_rows = (
            await db.execute(
                select(TaskExecutionLog.id, TaskExecutionLog.status, TaskExecutionLog.created_at, ScheduledTask.name)
                .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
                .where(*log_filters_recent)
                .order_by(TaskExecutionLog.created_at.desc())
                .limit(6)
            )
        ).all()
    except Exception as exc:
        logger.warning("Dashboard recent events query failed: %s", exc)
        recent_log_rows = []

    color_map = {
        "failed": "red",
        "success": "green",
        "running": "blue",
        "pending": "gold",
    }
    status_text = {
        "failed": "执行失败",
        "success": "执行成功",
        "running": "执行中",
        "pending": "等待执行",
    }
    events = [
        {
            "id": log_id,
            "title": f"{status_text.get(status, '任务更新')} · {task_name or '未命名任务'}",
            "time": _relative_time(created_at),
            "color": color_map.get(status, "gray"),
            "log_id": log_id,
        }
        for log_id, status, created_at, task_name in recent_log_rows
    ]

    try:
        trend_rows = (
            await db.execute(
                select(TaskExecutionLog.created_at, TaskExecutionLog.status)
                .outerjoin(ScheduledTask, TaskExecutionLog.task_id == ScheduledTask.id)
                .where(TaskExecutionLog.created_at >= trend_start, *log_filters_recent)
                .order_by(TaskExecutionLog.created_at.asc())
            )
        ).all()
    except Exception as exc:
        logger.warning("Dashboard trend query failed: %s", exc)
        trend_rows = []

    trend_bucket: dict[str, dict[str, int]] = {}
    for day_offset in range(trend_days):
        day = trend_start + timedelta(days=day_offset)
        key = day.strftime("%m-%d")
        trend_bucket[key] = {"total": 0, "failed": 0}

    for created_at, status in trend_rows:
        if not created_at:
            continue
        key = created_at.strftime("%m-%d")
        if key not in trend_bucket:
            continue
        trend_bucket[key]["total"] += 1
        if status == "failed":
            trend_bucket[key]["failed"] += 1

    trend_dates = list(trend_bucket.keys())
    trend_total_runs = [trend_bucket[d]["total"] for d in trend_dates]
    trend_failed_runs = [trend_bucket[d]["failed"] for d in trend_dates]

    notices = []
    scope_label = "当前范围"
    if group_name:
        scope_label = f"分组 {group_name}"
    elif project_name:
        scope_label = f"项目 {project_name}"

    if offline_servers > 0:
        notices.append(
            {
                "title": f"当前有 {offline_servers} 台离线主机，建议检查网络或 JumpServer 资产状态",
                "time": _relative_time(now),
            }
        )
    if failed_runs > 0:
        notices.append(
            {
                "title": f"今日任务失败 {failed_runs} 次，请优先查看失败日志",
                "time": _relative_time(now),
            }
        )
    notices.append(
        {
            "title": f"{scope_label}已启用 {enabled_tasks}/{total_tasks} 个定时任务",
            "time": _relative_time(now),
        }
    )
    notices = notices[:3]

    health = [
        {
            "name": "Celery Worker",
            "status": "正常" if celery_health.get("ok") else "异常",
            "color": "green" if celery_health.get("ok") else "red",
            "desc": f"在线 Worker: {len(celery_health.get('workers') or [])}",
        },
        {
            "name": "任务调度 Beat",
            "status": "正常" if celery_health.get("beat_healthy") else "关注",
            "color": "green" if celery_health.get("beat_healthy") else "gold",
            "desc": celery_health.get("detail") or "队列健康检查",
        },
        {
            "name": "执行稳定性（24h）",
            "status": "稳定" if last_24h_failed_runs == 0 else "波动",
            "color": "green" if last_24h_failed_runs == 0 else "gold",
            "desc": f"24小时失败 {last_24h_failed_runs} 次",
        },
    ]

    return {
        "code": 200,
        "message": "success",
        "data": {
            "generated_at": now.isoformat(),
            "filters": {
                "project_id": project_id,
                "project_name": project_name,
                "group_id": group_id,
                "group_name": group_name,
            },
            "summary": {
                "active_users": active_users,
                "total_users": total_users,
                "knowledge_bases": knowledge_bases,
                "documents": documents,
                "indexed_documents": indexed_documents,
                "servers": servers,
                "online_servers": online_servers,
                "today_runs": today_runs,
                "failed_runs": failed_runs,
                "today_chats": today_chats,
                "chunks": chunks,
                "enabled_tasks": enabled_tasks,
                "total_tasks": total_tasks,
                "success_rate": success_rate,
            },
            "notices": notices,
            "health": health,
            "events": events,
            "trends": {
                "dates": trend_dates,
                "total_runs": trend_total_runs,
                "failed_runs": trend_failed_runs,
            },
        },
    }
