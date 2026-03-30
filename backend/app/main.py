from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core import config
from app.db.database import init_db
from app.api.common import auth_router
from app.api.system import users_router, roles_router, menus_router
from app.api.agent import rag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时执行清理（如果需要）


app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description="AgenticOps - 智能知识库平台",
    lifespan=lifespan,
)

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


@app.get("/")
async def root():
    return {"message": "AgenticOps API", "version": config.VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
