"""Ops 模块路由"""

from fastapi import APIRouter
from app.api.ops.servers import router as servers_router
from app.api.ops.scripts import router as scripts_router
from app.api.ops.tasks import router as tasks_router
from app.api.ops.logs import router as logs_router

router = APIRouter(prefix="/api/ops")

# 注册子路由
router.include_router(servers_router)
router.include_router(scripts_router)
router.include_router(tasks_router)
router.include_router(logs_router)
