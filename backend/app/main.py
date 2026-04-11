from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import asyncio
import sys

from app.core import config
from app.core.request_context import reset_current_request, set_current_request
from app.api.auth import auth_router
from app.api.agent import rag_router
from app.api.system import users_router, roles_router, menus_router
from app.api.common.logs import router as logs_router
from app.api.ops import router as ops_router
from app.db.database import engine


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时不再自动创建表，改为手动运行 init_db.py 初始化
    # await init_db()  # 已禁用自动初始化，避免创建未使用的 Agent 表
    yield
    await engine.dispose()


app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description="AgenticOps - 智能知识库平台",
    lifespan=lifespan,
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = set_current_request(request)
        try:
            response = await call_next(request)
            return response
        finally:
            reset_current_request(token)


app.add_middleware(RequestContextMiddleware)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(menus_router, prefix="/api")
app.include_router(rag_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(ops_router)  # Ops 模块路由（服务器/脚本/任务/日志）


@app.get("/")
async def root():
    return {"message": "AgenticOps API", "version": config.VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
