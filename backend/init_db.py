"""
数据库初始化脚本
使用方式: python init_db.py
功能: 
  - 创建数据库（如果不存在）
  - 删除所有旧表并重新创建（回到项目最初状态）
  - 初始化基础数据（管理员、角色、菜单）
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


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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
    from sqlalchemy import text

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
    # 导入运维管理模块的模型（Ops）
    from app.models.ops import (  # noqa: F401
        Server,
        Script,
        ScheduledTask,
        TaskExecutionLog,
        OpsProject,
        OpsGroup,
    )
    # 导入操作日志模块的模型
    from app.models.log import OperationLog  # noqa: F401
    # 导入智能问数模块的模型
    from app.models.dataquery import (  # noqa: F401
        DataSource,
        TableMetadata,
        QueryHistory,
    )

    engine = create_async_engine(config.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        if force_reset:
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

            # 删除数据库中所有现有表（包括历史遗留表，如 server/server_group）
            result = await conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = DATABASE()
                    """
                )
            )
            table_names = [row[0] for row in result.fetchall()]
            for table_name in table_names:
                await conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))

            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            print(f"      已清空旧数据表 {len(table_names)} 张")
        await conn.run_sync(Base.metadata.create_all)

        # 兼容老库：补充 ops_scheduled_task.updated_by 字段
        result = await conn.execute(
            text("SHOW COLUMNS FROM ops_scheduled_task LIKE 'updated_by'")
        )
        if result.first() is None:
            await conn.execute(
                text(
                    "ALTER TABLE ops_scheduled_task "
                    "ADD COLUMN updated_by VARCHAR(50) NULL COMMENT '修改人' AFTER created_by"
                )
            )
            print("      已新增字段: ops_scheduled_task.updated_by")

        # 兼容老库：补充脚本/任务的项目和分组字段
        for table_name in ("ops_script", "ops_scheduled_task"):
            for col_name, col_ddl in (
                ("project_id", "INT NULL COMMENT '所属项目ID'"),
                ("group_id", "INT NULL COMMENT '所属分组ID'"),
            ):
                col_result = await conn.execute(
                    text(f"SHOW COLUMNS FROM {table_name} LIKE '{col_name}'")
                )
                if col_result.first() is None:
                    await conn.execute(
                        text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_ddl}")
                    )
                    print(f"      已新增字段: {table_name}.{col_name}")

        # 为高频日志查询补齐索引（兼容已有库的增量初始化）
        result = await conn.execute(text("SHOW INDEX FROM ops_task_execution_log"))
        existing_indexes = {row[2] for row in result.fetchall()}
        index_defs = {
            "idx_ops_log_created_at": "created_at",
            "idx_ops_log_status_created_at": "status, created_at",
            "idx_ops_log_task_created_at": "task_id, created_at",
            "idx_ops_log_server_created_at": "server_id, created_at",
        }
        for index_name, columns in index_defs.items():
            if index_name in existing_indexes:
                continue
            await conn.execute(
                text(
                    f"ALTER TABLE ops_task_execution_log "
                    f"ADD INDEX {index_name} ({columns})"
                )
            )
            print(f"      已创建索引: {index_name}")

        # 为脚本/任务的项目分组字段补齐索引
        for table_name, idx_defs in {
            "ops_script": {
                "idx_ops_script_project_id": "project_id",
                "idx_ops_script_group_id": "group_id",
            },
            "ops_scheduled_task": {
                "idx_ops_task_project_id": "project_id",
                "idx_ops_task_group_id": "group_id",
            },
        }.items():
            idx_result = await conn.execute(text(f"SHOW INDEX FROM {table_name}"))
            existing_indexes = {row[2] for row in idx_result.fetchall()}
            for idx_name, idx_cols in idx_defs.items():
                if idx_name in existing_indexes:
                    continue
                await conn.execute(
                    text(f"ALTER TABLE {table_name} ADD INDEX {idx_name} ({idx_cols})")
                )
                print(f"      已创建索引: {idx_name}")

        # 兼容老库：补齐默认项目/分组并回填历史脚本任务
        await conn.execute(
            text(
                "INSERT INTO ops_project (name, code, description, created_by) "
                "SELECT '默认项目', 'default', '系统默认项目', 'system' "
                "FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM ops_project WHERE code = 'default')"
            )
        )
        project_result = await conn.execute(
            text("SELECT id FROM ops_project WHERE code = 'default' LIMIT 1")
        )
        default_project_id = project_result.scalar()

        await conn.execute(
            text(
                "INSERT INTO ops_group (project_id, name, description, created_by) "
                "SELECT :project_id, '未分组', '系统默认分组', 'system' "
                "FROM DUAL WHERE NOT EXISTS "
                "(SELECT 1 FROM ops_group WHERE project_id = :project_id AND name = '未分组')"
            ),
            {"project_id": default_project_id},
        )
        group_result = await conn.execute(
            text(
                "SELECT id FROM ops_group "
                "WHERE project_id = :project_id AND name = '未分组' LIMIT 1"
            ),
            {"project_id": default_project_id},
        )
        default_group_id = group_result.scalar()

        await conn.execute(
            text(
                "UPDATE ops_script SET "
                "project_id = COALESCE(project_id, :project_id), "
                "group_id = COALESCE(group_id, :group_id) "
                "WHERE project_id IS NULL OR group_id IS NULL"
            ),
            {"project_id": default_project_id, "group_id": default_group_id},
        )
        await conn.execute(
            text(
                "UPDATE ops_scheduled_task SET "
                "project_id = COALESCE(project_id, :project_id), "
                "group_id = COALESCE(group_id, :group_id) "
                "WHERE project_id IS NULL OR group_id IS NULL"
            ),
            {"project_id": default_project_id, "group_id": default_group_id},
        )
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
            # ---- 智能问数 ----
            {
                "name": "智能问数",
                "code": "dataquery",
                "path": "/dataquery",
                "icon": "ConsoleSql",
                "type": "directory",
                "sort_order": 2,
                "parent_id": None,
                "description": "智能问数模块",
            },
            {
                "name": "数据源管理",
                "code": "dataquery:datasources",
                "path": "/dataquery/datasources",
                "icon": "Database",
                "type": "menu",
                "sort_order": 1,
                "parent_code": "dataquery",
                "component": "dataquery/DataSourceList",
                "description": "管理数据库连接与表结构",
            },
            {
                "name": "智能问数",
                "code": "dataquery:chat",
                "path": "/dataquery/chat",
                "icon": "Search",
                "type": "menu",
                "sort_order": 2,
                "parent_code": "dataquery",
                "component": "dataquery/QueryChat",
                "description": "自然语言查询数据库",
            },
            {
                "name": "数据源创建",
                "code": "dataquery:datasource:create",
                "type": "button",
                "sort_order": 1,
                "parent_code": "dataquery:datasources",
                "description": "创建数据源连接",
            },
            {
                "name": "数据源编辑",
                "code": "dataquery:datasource:edit",
                "type": "button",
                "sort_order": 2,
                "parent_code": "dataquery:datasources",
                "description": "编辑数据源连接",
            },
            {
                "name": "数据源删除",
                "code": "dataquery:datasource:delete",
                "type": "button",
                "sort_order": 3,
                "parent_code": "dataquery:datasources",
                "description": "删除数据源连接",
            },
            # ---- 运维管理 ----
            {
                "name": "运维管理",
                "code": "ops",
                "path": "/ops",
                "icon": "Tool",
                "type": "directory",
                "sort_order": 3,
                "parent_id": None,
                "description": "运维管理模块",
            },
            {
                "name": "服务器列表",
                "code": "ops:servers",
                "path": "/ops/servers",
                "icon": "Desktop",
                "type": "menu",
                "sort_order": 1,
                "parent_code": "ops",
                "component": "ops/ServerList",
                "description": "服务器列表管理",
            },
            {
                "name": "脚本管理",
                "code": "ops:scripts",
                "path": "/ops/scripts",
                "icon": "Code",
                "type": "menu",
                "sort_order": 2,
                "parent_code": "ops",
                "component": "ops/ScriptList",
                "description": "脚本库管理",
            },
            {
                "name": "定时任务",
                "code": "ops:tasks",
                "path": "/ops/tasks",
                "icon": "ClockCircle",
                "type": "menu",
                "sort_order": 3,
                "parent_code": "ops",
                "component": "ops/TaskList",
                "description": "定时任务管理",
            },
            {
                "name": "执行日志",
                "code": "ops:logs",
                "path": "/ops/logs",
                "icon": "File",
                "type": "menu",
                "sort_order": 4,
                "parent_code": "ops",
                "component": "ops/LogList",
                "description": "任务执行日志",
            },
            {
                "name": "项目分组",
                "code": "ops:groups",
                "path": "/ops/groups",
                "icon": "Collection",
                "type": "menu",
                "sort_order": 0,
                "parent_code": "ops",
                "component": "ops/GroupManagement",
                "description": "项目与分组管理",
            },
            {
                "name": "项目查询",
                "code": "ops:projects:list",
                "type": "button",
                "sort_order": 1,
                "parent_code": "ops:groups",
                "description": "查询项目列表",
            },
            {
                "name": "项目创建",
                "code": "ops:projects:create",
                "type": "button",
                "sort_order": 2,
                "parent_code": "ops:groups",
                "description": "创建项目",
            },
            {
                "name": "项目更新",
                "code": "ops:projects:update",
                "type": "button",
                "sort_order": 3,
                "parent_code": "ops:groups",
                "description": "更新项目",
            },
            {
                "name": "项目删除",
                "code": "ops:projects:delete",
                "type": "button",
                "sort_order": 4,
                "parent_code": "ops:groups",
                "description": "删除项目",
            },
            {
                "name": "分组查询",
                "code": "ops:groups:list",
                "type": "button",
                "sort_order": 5,
                "parent_code": "ops:groups",
                "description": "查询分组列表",
            },
            {
                "name": "分组创建",
                "code": "ops:groups:create",
                "type": "button",
                "sort_order": 6,
                "parent_code": "ops:groups",
                "description": "创建分组",
            },
            {
                "name": "分组更新",
                "code": "ops:groups:update",
                "type": "button",
                "sort_order": 7,
                "parent_code": "ops:groups",
                "description": "更新分组",
            },
            {
                "name": "分组删除",
                "code": "ops:groups:delete",
                "type": "button",
                "sort_order": 8,
                "parent_code": "ops:groups",
                "description": "删除分组",
            },
            {
                "name": "系统管理",
                "code": "system",
                "path": "/system",
                "icon": "Setting",
                "type": "directory",
                "sort_order": 4,
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
