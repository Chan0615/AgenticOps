from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.models import Role, RoleMenu, User, UserRole
from app.schemas.system.role import RoleCreate, RoleUpdate


async def get_role_by_id(db: AsyncSession, role_id: int) -> Optional[Role]:
    """通过ID获取角色"""
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions).selectinload(RoleMenu.menu))
        .where(Role.id == role_id)
    )
    return result.scalar_one_or_none()


async def get_role_by_code(db: AsyncSession, code: str) -> Optional[Role]:
    """通过代码获取角色"""
    result = await db.execute(select(Role).where(Role.code == code))
    return result.scalar_one_or_none()


async def create_role(db: AsyncSession, role_in: RoleCreate) -> Role:
    """创建角色"""
    role = Role(
        name=role_in.name,
        code=role_in.code,
        description=role_in.description,
        sort_order=role_in.sort_order,
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)

    # 添加菜单权限
    if role_in.menu_ids:
        for menu_id in role_in.menu_ids:
            role_menu = RoleMenu(role_id=role.id, menu_id=menu_id)
            db.add(role_menu)
        await db.commit()
        await db.refresh(role)

    return role


async def update_role(
    db: AsyncSession, role_id: int, role_in: RoleUpdate
) -> Optional[Role]:
    """更新角色"""
    role = await get_role_by_id(db, role_id)
    if not role:
        return None

    update_data = role_in.model_dump(exclude_unset=True)
    menu_ids = update_data.pop("menu_ids", None)

    for field, value in update_data.items():
        setattr(role, field, value)

    # 更新菜单权限
    if menu_ids is not None:
        # 删除旧的权限
        await db.execute(delete(RoleMenu).where(RoleMenu.role_id == role_id))

        # 添加新权限
        for menu_id in menu_ids:
            role_menu = RoleMenu(role_id=role_id, menu_id=menu_id)
            db.add(role_menu)

    await db.commit()
    await db.refresh(role)
    return role


async def delete_role(db: AsyncSession, role_id: int) -> bool:
    """删除角色"""
    role = await get_role_by_id(db, role_id)
    if not role:
        return False

    await db.delete(role)
    await db.commit()
    return True


async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Role]:
    """获取角色列表"""
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions).selectinload(RoleMenu.menu))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_role_users(db: AsyncSession, role_id: int) -> List[User]:
    """获取角色下的用户列表"""
    result = await db.execute(
        select(User)
        .join(UserRole, UserRole.user_id == User.id)
        .where(UserRole.role_id == role_id)
    )
    return result.scalars().all()
