from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.system.menu import MenuCreate, MenuUpdate, MenuResponse
from app.schemas.system.user import UserResponse
from app.api.common.auth import get_current_user
from app.crud.system import menu as menu_crud

router = APIRouter(prefix="/menus", tags=["菜单管理"])


@router.get("/my", response_model=List[MenuResponse])
async def get_my_menus(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户的菜单"""
    if current_user.is_superuser:
        menus = await menu_crud.get_all_menus(db)
    else:
        menus = await menu_crud.get_user_menus(db, current_user.id)
    return [MenuResponse.model_validate(m) for m in menus]


@router.get("/", response_model=List[MenuResponse])
async def get_menus(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取菜单列表（树形结构）"""
    menus = await menu_crud.get_all_menus(db)
    return [MenuResponse.model_validate(m) for m in menus]


@router.get("/all", response_model=List[MenuResponse])
async def get_all_menus_flat(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取所有菜单（扁平结构）"""
    menus = await menu_crud.get_menus(db, skip=skip, limit=limit)
    return [MenuResponse.model_validate(m) for m in menus]


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取指定菜单"""
    menu = await menu_crud.get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
    return MenuResponse.model_validate(menu)


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_in: MenuCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建菜单"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限创建菜单"
        )

    # 检查菜单代码是否已存在
    existing_menu = await menu_crud.get_menu_by_code(db, menu_in.code)
    if existing_menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="菜单代码已存在"
        )

    menu = await menu_crud.create_menu(db, menu_in)
    return MenuResponse.model_validate(menu)


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu_update: MenuUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新菜单"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限更新菜单"
        )

    menu = await menu_crud.update_menu(db, menu_id, menu_update)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
    return MenuResponse.model_validate(menu)


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除菜单"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="没有权限删除菜单"
        )

    success = await menu_crud.delete_menu(db, menu_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
    return {"message": "菜单删除成功"}
