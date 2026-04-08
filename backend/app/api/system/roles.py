from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.system.role import RoleCreate, RoleUpdate, RoleResponse
from app.schemas.system.user import UserResponse
from app.api.auth.auth import get_current_user
from app.crud.system import role as role_crud


router = APIRouter(prefix="/roles", tags=["角色管理"])


@router.get("/", response_model=List[RoleResponse])
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取角色列表"""
    roles = await role_crud.get_roles(db, skip=skip, limit=limit)
    return [RoleResponse.model_validate(r) for r in roles]


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取指定角色"""
    role = await role_crud.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return RoleResponse.model_validate(role)


@router.get("/{role_id}/users", response_model=List[UserResponse])
async def get_role_users(
    role_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取角色下的用户列表"""
    role = await role_crud.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    users = await role_crud.get_role_users(db, role_id)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{role_id}/menus", response_model=List[int])
async def get_role_menu_ids(
    role_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取角色关联的菜单ID列表"""
    role = await role_crud.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return [p.menu_id for p in role.permissions]


@router.put("/{role_id}/menus")
async def update_role_menus(
    role_id: int,
    menu_ids: List[int],
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新角色关联的菜单"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="没有权限")
    role = await role_crud.update_role(db, role_id, RoleUpdate(menu_ids=menu_ids))
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return {"message": "更新成功", "menu_ids": menu_ids}


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建角色"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限创建角色"
        )
    existing_role = await role_crud.get_role_by_code(db, role_in.code)
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="角色代码已存在"
        )
    role = await role_crud.create_role(db, role_in)
    return RoleResponse.model_validate(role)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新角色"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限更新角色"
        )
    role = await role_crud.update_role(db, role_id, role_update)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return RoleResponse.model_validate(role)


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除角色"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限删除角色"
        )
    success = await role_crud.delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return {"message": "角色删除成功"}
