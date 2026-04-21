"""Ops 模块路由"""

from fastapi import APIRouter
from app.api.ops.servers import router as servers_router
from app.api.ops.groups import router as groups_router
from app.api.ops.scripts import router as scripts_router
from app.api.ops.tasks import router as tasks_router
from app.api.ops.logs import router as logs_router
from app.api.ops.dashboard import router as dashboard_router
from app.api.ops.ai_chat import router as ai_chat_router

router = APIRouter()

# 注册子路由（子路由已包含完整前缀）
router.include_router(servers_router)
router.include_router(groups_router)
router.include_router(scripts_router)
router.include_router(tasks_router)
router.include_router(logs_router)
router.include_router(dashboard_router)
router.include_router(ai_chat_router)  # 运维 AI 助手
