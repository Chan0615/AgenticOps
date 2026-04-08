from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.agent import router as agent_router
from app.api.system import users_router, roles_router, menus_router
from app.api.common.logs import router as logs_router
from app.api.ops import router as ops_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时不自动初始化数据库（使用 init_db.py 手动初始化）
    yield
    # 关闭时执行清理（如果需要）


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AgenticOps - 智能平台后端API",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(menus_router, prefix="/api")
app.include_router(agent_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(ops_router)  # Ops 模块路由


@app.get("/")
async def root():
    return {"message": "AgenticOps API", "version": settings.VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
