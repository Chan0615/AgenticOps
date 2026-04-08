"""
数据库初始化脚本
使用方式: python init_db.py
功能: 创建数据库、建表、初始化基础数据（管理员、角色、菜单）
"""

import asyncio
import sys
import os

# 确保能导入 app 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymysql
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core import config
from app.core.security import get_password_hash


def _get_mysql_default() -> dict:
    """获取默认 MySQL 配置"""
    return config._get("mysql", "default")


def create_database():
    """创建数据库（如果不存在）"""
    db_cfg = _get_mysql_default()
    print(f"[1/4] 创建数据库 '{db_cfg['database']}' ...")
    conn = pymysql.connect(
        host=db_cfg["host"],
        port=db_cfg["port"],
        user=db_cfg["user"],
        password=db_cfg["password"],
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_cfg['database']}` "
                f"DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
        print(f"      数据库 '{db_cfg['database']}' 就绪")
    finally:
        conn.close()


async def create_tables(force_reset: bool = False):
    """创建所有表"""
    print("[2/4] 创建数据表 ...")
    from app.db.database import Base
    # 导入系统管理模块和 Agent RAG 模块的模型
    from app.models.models import User, Role, UserRole, Menu, RoleMenu  # noqa: F401
    from app.models.agent import (  # noqa: F401
        KnowledgeBase,
        Document,
        AgentDocumentChunk,
        Conversation,
        ConversationMessage
    )

    engine = create_async_engine(config.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        if force_reset:
            # 先删除有外键依赖的表，避免外键约束错误
            from sqlalchemy import text
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            await conn.run_sync(Base.metadata.drop_all)
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            print("      已清空旧数据表")
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("      数据表创建完成")


async def seed_data():
    """初始化基础数据"""
    print("[3/4] 初始化基础数据 ...")

    from app.db.database import Base
    from app.models.models import User, Role, UserRole, Menu, RoleMenu

    engine = create_async_engine(config.DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        from sqlalchemy import select

        result = await session.execute(select(User).where(User.username == "admin"))
        if result.scalar_one_or_none():
            print("      数据已存在，跳过初始化")
            await engine.dispose()
            print("[4/4] 初始化完成！")
            return

        # ---------- 菜单 ----------
        menus = [
            {
                "name": "仪表盘",
                "code": "dashboard",
                "path": "/dashboard",
                "icon": "DataBoard",
                "type": "menu",
                "sort_order": 0,
                "parent_id": None,
                "description": "数据概览",
            },
            {
                "name": "RAG知识库",
                "code": "rag",
                "path": "/rag",
                "icon": "Brain",
                "type": "directory",
                "sort_order": 1,
                "parent_id": None,
                "description": "RAG 知识库模块",
            },
            {
                "name": "AI 问答",
                "code": "rag:chat",
                "path": "/rag/chat",
                "icon": "ChatDotRound",
                "type": "menu",
                "sort_order": 1,
                "parent_code": "rag",
                "component": "rag/Chat",
                "description": "智能问答",
            },
            {
                "name": "知识库管理",
                "code": "rag:knowledge",
                "path": "/rag/knowledge",
                "icon": "Collection",
                "type": "menu",
                "sort_order": 2,
                "parent_code": "rag",
                "component": "rag/KnowledgeBase",
                "description": "知识库文档管理",
            },
            {
                "name": "系统管理",
                "code": "system",
                "path": "/system",
                "icon": "Setting",
                "type": "directory",
                "sort_order": 2,
                "parent_id": None,
                "description": "系统管理模块",
            },
            {
                "name": "用户管理",
                "code": "system:user",
                "path": "/system/users",
                "icon": "User",
                "type": "menu",
                "sort_order": 1,
                "parent_code": "system",
                "component": "system/users/index",
                "description": "用户管理",
            },
            {
                "name": "角色管理",
                "code": "system:role",
                "path": "/system/roles",
                "icon": "UserFilled",
                "type": "menu",
                "sort_order": 2,
                "parent_code": "system",
                "component": "system/roles/index",
                "description": "角色管理",
            },
            {
                "name": "菜单管理",
                "code": "system:menu",
                "path": "/system/menus",
                "icon": "Menu",
                "type": "menu",
                "sort_order": 3,
                "parent_code": "system",
                "component": "system/menus/index",
                "description": "菜单管理",
            },
            {
                "name": "用户查询",
                "code": "system:user:list",
                "type": "button",
                "sort_order": 1,
                "parent_code": "system:user",
                "description": "查询用户列表",
            },
            {
                "name": "用户创建",
                "code": "system:user:create",
                "type": "button",
                "sort_order": 2,
                "parent_code": "system:user",
                "description": "创建用户",
            },
            {
                "name": "用户更新",
                "code": "system:user:update",
                "type": "button",
                "sort_order": 3,
                "parent_code": "system:user",
                "description": "更新用户",
            },
            {
                "name": "用户删除",
                "code": "system:user:delete",
                "type": "button",
                "sort_order": 4,
                "parent_code": "system:user",
                "description": "删除用户",
            },
            {
                "name": "角色查询",
                "code": "system:role:list",
                "type": "button",
                "sort_order": 1,
                "parent_code": "system:role",
                "description": "查询角色列表",
            },
            {
                "name": "角色创建",
                "code": "system:role:create",
                "type": "button",
                "sort_order": 2,
                "parent_code": "system:role",
                "description": "创建角色",
            },
            {
                "name": "角色更新",
                "code": "system:role:update",
                "type": "button",
                "sort_order": 3,
                "parent_code": "system:role",
                "description": "更新角色",
            },
            {
                "name": "角色删除",
                "code": "system:role:delete",
                "type": "button",
                "sort_order": 4,
                "parent_code": "system:role",
                "description": "删除角色",
            },
            {
                "name": "菜单查询",
                "code": "system:menu:list",
                "type": "button",
                "sort_order": 1,
                "parent_code": "system:menu",
                "description": "查询菜单列表",
            },
            {
                "name": "菜单创建",
                "code": "system:menu:create",
                "type": "button",
                "sort_order": 2,
                "parent_code": "system:menu",
                "description": "创建菜单",
            },
            {
                "name": "菜单更新",
                "code": "system:menu:update",
                "type": "button",
                "sort_order": 3,
                "parent_code": "system:menu",
                "description": "更新菜单",
            },
            {
                "name": "菜单删除",
                "code": "system:menu:delete",
                "type": "button",
                "sort_order": 4,
                "parent_code": "system:menu",
                "description": "删除菜单",
            },
        ]

        menu_map = {}
        for m in menus:
            parent_code = m.pop("parent_code", None)
            menu = Menu(**m)
            if parent_code and parent_code in menu_map:
                menu.parent_id = menu_map[parent_code].id
            session.add(menu)
            await session.flush()
            menu_map[menu.code] = menu

        print(f"      创建菜单 {len(menus)} 条")

        # ---------- 角色 ----------
        admin_role = Role(
            name="超级管理员", code="admin", description="拥有所有权限", sort_order=1
        )
        user_role = Role(
            name="普通用户", code="user", description="普通用户角色", sort_order=2
        )
        session.add_all([admin_role, user_role])
        await session.flush()
        print(f"      创建角色 2 个")

        # ---------- 角色-菜单关联 ----------
        for menu in menu_map.values():
            session.add(RoleMenu(role_id=admin_role.id, menu_id=menu.id))
        if "dashboard" in menu_map:
            session.add(
                RoleMenu(role_id=user_role.id, menu_id=menu_map["dashboard"].id)
            )
        print(f"      角色菜单关联完成")

        # ---------- 管理员用户 ----------
        admin_user = User(
            username="admin",
            email="admin@agenticops.com",
            phone="13800000000",
            password_hash=get_password_hash("admin123"),
            full_name="系统管理员",
            status=True,
            is_superuser=True,
        )
        session.add(admin_user)
        await session.flush()
        session.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
        print(f"      创建管理员用户 admin / admin123")

        await session.commit()

    await engine.dispose()
    print("[4/4] 初始化完成！")


async def main():
    create_database()
    await create_tables(force_reset=True)
    await seed_data()
    print("\n✅ 数据库初始化成功！")
    print(f"   管理员账号: admin  密码: admin123")


if __name__ == "__main__":
    asyncio.run(main())
