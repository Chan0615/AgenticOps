from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.schemas.system.user import UserCreate, UserResponse, UserUpdate
from app.schemas.common.auth import UserLogin, TokenResponse, RefreshTokenRequest
from app.crud.system import user as user_crud
from app.core.security import create_tokens, decode_token, verify_password, get_password_hash
from app.core.log_decorator import log_operation

router = APIRouter(prefix="/auth", tags=["认证"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = await user_crud.get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@log_operation(module="认证模块", action="用户注册", description="新用户注册")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否存在
    existing_user = await user_crud.get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否存在
    existing_email = await user_crud.get_user_by_email(db, user_in.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建用户
    user = await user_crud.create_user(db, user_in)
    
    # 创建令牌
    tokens = create_tokens(user.id, user.username)
    user_response = UserResponse.model_validate(user)
    
    return TokenResponse(**tokens, user=user_response)


@router.post("/login", response_model=TokenResponse)
@log_operation(module="认证模块", action="用户登录", description="用户登录系统")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    user = await user_crud.authenticate_user(db, user_in.username, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    tokens = create_tokens(user.id, user.username)
    user_response = UserResponse.model_validate(user)
    
    return TokenResponse(**tokens, user=user_response)


@router.post("/refresh", response_model=TokenResponse)
@log_operation(module="认证模块", action="刷新令牌", description="刷新访问令牌")
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """刷新令牌"""
    payload = decode_token(request.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    user_id = payload.get("sub")
    user = await user_crud.get_user_by_id(db, int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    tokens = create_tokens(user.id, user.username)
    user_response = UserResponse.model_validate(user)
    
    return TokenResponse(**tokens, user=user_response)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user


@router.put("/me", response_model=UserResponse)
@log_operation(module="认证模块", action="更新个人信息", description="更新当前用户信息")
async def update_me(
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    updated_user = await user_crud.update_user(db, current_user.id, user_update)
    return UserResponse.model_validate(updated_user)


@router.post("/change-password")
@log_operation(module="认证模块", action="修改密码", description="用户修改登录密码")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改密码"""
    user = await user_crud.get_user_by_id(db, current_user.id)
    
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    user.password_hash = get_password_hash(new_password)
    await db.commit()
    
    return {"message": "密码修改成功"}
