
# Common API 模块（已废弃，仅保留 auth 导入以兼容）
from app.api.auth.auth import router as auth_router

__all__ = ["auth_router"]
