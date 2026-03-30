from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.models import Menu, UserRole, RoleMenu
from app.schemas.system.menu import MenuCreate, MenuUpdate


async def get_menu_by_id(db: AsyncSession, menu_id: int) -> Optional[Menu]:
    """通过ID获取菜单"""
    result = await db.execute(
        select(Menu).options(selectinload(Menu.children)).where(Menu.id == menu_id)
    )
    return result.scalar_one_or_none()


async def get_menu_by_code(db: AsyncSession, code: str) -> Optional[Menu]:
    """通过代码获取菜单"""
    result = await db.execute(select(Menu).where(Menu.code == code))
    return result.scalar_one_or_none()


async def create_menu(db: AsyncSession, menu_in: MenuCreate) -> Menu:
    """创建菜单"""
    menu = Menu(
        name=menu_in.name,
        code=menu_in.code,
        path=menu_in.path,
        component=menu_in.component,
        icon=menu_in.icon,
        parent_id=menu_in.parent_id,
        sort_order=menu_in.sort_order,
        type=menu_in.type,
        meta=menu_in.meta,
        description=menu_in.description,
    )
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def update_menu(
    db: AsyncSession, menu_id: int, menu_in: MenuUpdate
) -> Optional[Menu]:
    """更新菜单"""
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        return None

    update_data = menu_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(menu, field, value)

    await db.commit()
    await db.refresh(menu)
    return menu


async def delete_menu(db: AsyncSession, menu_id: int) -> bool:
    """删除菜单"""
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        return False

    await db.delete(menu)
    await db.commit()
    return True


async def get_menus(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Menu]:
    """获取菜单列表"""
    result = await db.execute(
        select(Menu)
        .options(selectinload(Menu.children))
        .where(Menu.parent_id == None)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_all_menus(db: AsyncSession) -> List[Menu]:
    """获取所有菜单（树形结构）"""
    result = await db.execute(
        select(Menu)
        .options(selectinload(Menu.children))
        .where(Menu.parent_id == None)
        .order_by(Menu.sort_order)
    )
    return result.scalars().all()


async def get_user_menus(db: AsyncSession, user_id: int) -> List[Menu]:
    """获取用户拥有的菜单（树形结构）"""
    from sqlalchemy import distinct

    result = await db.execute(
        select(Menu)
        .options(selectinload(Menu.children))
        .where(Menu.parent_id == None)
        .where(
            Menu.id.in_(
                select(RoleMenu.menu_id)
                .join(UserRole, UserRole.role_id == RoleMenu.role_id)
                .where(UserRole.user_id == user_id)
            )
        )
        .order_by(Menu.sort_order)
    )
    return result.scalars().all()
