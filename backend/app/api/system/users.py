from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.system.user import UserCreate, UserResponse, UserUpdate
from app.api.auth.auth import get_current_user
from app.crud.system import user as user_crud

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取用户列表"""
    users = await user_crud.get_users(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取指定用户"""
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return UserResponse.model_validate(user)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建用户（仅管理员）"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限创建用户"
        )

    # 检查用户名是否存在
    existing_user = await user_crud.get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在"
        )

    user = await user_crud.create_user(db, user_in)
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新用户"""
    # 只有超级管理员或本人可以修改
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限修改该用户"
        )

    updated_user = await user_crud.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限删除用户"
        )

    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="不能删除自己"
        )

    success = await user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return {"message": "用户删除成功"}


@router.post("/{user_id}/reset-password")
async def reset_password(
    user_id: int,
    password_data: dict,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """重置用户密码（仅超级管理员）"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="只有超级管理员可以重置密码"
        )
    
    new_password = password_data.get("password")
    if not new_password or len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="密码长度至少6位"
        )
    
    from app.core.security import get_password_hash
    from app.models.user import User
    from sqlalchemy import select
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    
    return {"message": "密码重置成功"}
