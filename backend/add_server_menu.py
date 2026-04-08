"""
添加服务器管理菜单到数据库
使用方式: python add_server_menu.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core import config
from app.models.models import Menu


async def add_server_menus():
    """添加服务器管理菜单"""
    engine = create_async_engine(config.DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        from sqlalchemy import select

        # 检查服务器管理菜单是否已存在
        result = await session.execute(
            select(Menu).where(Menu.code == "server")
        )
        server_menu = result.scalar_one_or_none()

        if server_menu:
            print("服务器管理菜单已存在，跳过添加")
            await engine.dispose()
            return

        print("开始添加服务器管理菜单...")

        # 创建服务器管理主菜单
        server_menu = Menu(
            name="服务器管理",
            code="server",
            path="/server",
            icon="Server",
            type="directory",
            sort_order=2,
            parent_id=None,
            description="服务器管理模块",
        )
        session.add(server_menu)
        await session.flush()

        # 创建服务器列表子菜单
        server_list_menu = Menu(
            name="服务器列表",
            code="server:list",
            path="/server",
            icon="Desktop",
            type="menu",
            sort_order=1,
            parent_id=server_menu.id,
            component="server/ServerManagement",
            description="服务器列表管理",
        )
        session.add(server_list_menu)

        # 创建操作日志子菜单
        server_logs_menu = Menu(
            name="操作日志",
            code="server:logs",
            path="/server/logs",
            icon="File",
            type="menu",
            sort_order=2,
            parent_id=server_menu.id,
            component="server/OperationLogs",
            description="操作日志查看",
        )
        session.add(server_logs_menu)

        await session.commit()
        print("✅ 服务器管理菜单添加成功！")
        print("   - 服务器管理（目录）")
        print("   - 服务器列表（菜单）")
        print("   - 操作日志（菜单）")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(add_server_menus())
