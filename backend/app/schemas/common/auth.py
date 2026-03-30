from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.system.user import UserResponse


# ============ 认证相关 ============
class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
