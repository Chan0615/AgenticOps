"""智能问数模块路由"""

from fastapi import APIRouter
from app.api.dataquery.datasource import router as datasource_router
from app.api.dataquery.chat import router as chat_router

router = APIRouter()

# 注册子路由（子路由已包含完整前缀）
router.include_router(datasource_router)
router.include_router(chat_router)
