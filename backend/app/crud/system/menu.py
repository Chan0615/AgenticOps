from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.models import Menu


async def get_menu_by_id(db: AsyncSession, menu_id: int) -> Optional[Menu]:
    """根据ID获取菜单"""
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    return result.scalar_one_or_none()


async def get_menu_by_code(db: AsyncSession, code: str) -> Optional[Menu]:
    """根据代码获取菜单"""
    result = await db.execute(select(Menu).where(Menu.code == code))
    return result.scalar_one_or_none()


async def get_menu_list(
    db: AsyncSession, skip: int = 0, limit: int = 100, menu_type: Optional[str] = None
) -> List[Menu]:
    """获取菜单列表"""
    query = select(Menu)
    if menu_type:
        query = query.where(Menu.type == menu_type)
    query = query.offset(skip).limit(limit).order_by(Menu.sort_order)
    result = await db.execute(query)
    return result.scalars().all()


async def create_menu(db: AsyncSession, menu_data: dict) -> Menu:
    """创建菜单"""
    menu = Menu(**menu_data)
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def update_menu(db: AsyncSession, menu_id: int, menu_data) -> Optional[Menu]:
    """更新菜单"""
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        return None
    update_data = (
        menu_data.model_dump(exclude_unset=True)
        if hasattr(menu_data, "model_dump")
        else menu_data
    )
    for key, value in update_data.items():
        if value is not None:
            setattr(menu, key, value)
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


def _build_tree(menus: List[Menu]) -> List[dict]:
    """将扁平菜单列表构建为树形结构"""
    menu_map = {}
    for m in menus:
        menu_map[m.id] = {
            "id": m.id,
            "name": m.name,
            "code": m.code,
            "path": m.path,
            "component": m.component,
            "icon": m.icon,
            "parent_id": m.parent_id,
            "sort_order": m.sort_order,
            "type": m.type,
            "status": m.status,
            "meta": m.meta,
            "description": m.description,
            "created_at": m.created_at,
            "updated_at": m.updated_at,
            "children": [],
        }

    roots = []
    for item in menu_map.values():
        pid = item["parent_id"]
        if pid and pid in menu_map:
            menu_map[pid]["children"].append(item)
        else:
            roots.append(item)

    # 排序
    def sort_children(node):
        node["children"].sort(key=lambda x: x["sort_order"])
        for c in node["children"]:
            sort_children(c)

    roots.sort(key=lambda x: x["sort_order"])
    for r in roots:
        sort_children(r)

    return roots


async def get_all_menus(db: AsyncSession) -> List[dict]:
    """获取所有菜单（树形结构）"""
    result = await db.execute(select(Menu).order_by(Menu.sort_order))
    menus = result.scalars().all()
    return _build_tree(menus)


async def get_user_menus(db: AsyncSession, user_id: int) -> List[dict]:
    """获取用户拥有的菜单（树形结构）"""
    from app.models.models import UserRole, RoleMenu

    # 查出用户有权限的菜单ID
    result = await db.execute(
        select(Menu)
        .where(
            Menu.id.in_(
                select(RoleMenu.menu_id)
                .join(UserRole, UserRole.role_id == RoleMenu.role_id)
                .where(UserRole.user_id == user_id)
            )
        )
        .order_by(Menu.sort_order)
    )
    menus = result.scalars().all()

    # 收集所有需要展示的菜单ID（包含父级）
    show_ids = set()
    for m in menus:
        show_ids.add(m.id)
        if m.parent_id:
            show_ids.add(m.parent_id)

    # 取出这些菜单
    result = await db.execute(
        select(Menu).where(Menu.id.in_(show_ids)).order_by(Menu.sort_order)
    )
    all_menus = result.scalars().all()
    return _build_tree(all_menus)
