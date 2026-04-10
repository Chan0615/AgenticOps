"""
迁移 legacy /server 菜单到 /ops 菜单结构
默认预览（不落库）: python add_server_menu.py
执行迁移（落库）: python add_server_menu.py --apply
"""

import argparse
import asyncio
import os
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core import config
from app.models.models import Menu


def _menu_snapshot(menu: Menu) -> dict:
    return {
        "name": menu.name,
        "code": menu.code,
        "path": menu.path,
        "icon": menu.icon,
        "type": menu.type,
        "sort_order": menu.sort_order,
        "component": menu.component,
        "description": menu.description,
        "parent_id": menu.parent_id,
    }


def _print_changes(changes: list[str], dry_run: bool):
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n[{mode}] 变更计划/结果")
    if not changes:
        print("- 无需变更")
        return
    for idx, item in enumerate(changes, start=1):
        print(f"{idx}. {item}")


def _print_field_diff(before: dict, after: dict):
    focus_fields = ["name", "code", "path", "component"]
    for field in focus_fields:
        before_value = before.get(field)
        after_value = after.get(field)
        if before_value != after_value:
            print(f"   - {field}: {before_value!r} -> {after_value!r}")


async def migrate_server_menus_to_ops(dry_run: bool = True, verbose: bool = False):
    engine = create_async_engine(config.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    changes: list[str] = []

    async with async_session() as session:
        result = await session.execute(select(Menu))
        menus = result.scalars().all()

        by_code = {m.code: m for m in menus if m.code}

        ops_menu = by_code.get("ops")
        server_dir = by_code.get("server")

        if not ops_menu and server_dir and server_dir.type == "directory":
            before = _menu_snapshot(server_dir)
            server_dir.name = "运维管理"
            server_dir.code = "ops"
            server_dir.path = "/ops"
            server_dir.icon = "Tool"
            server_dir.description = "运维管理模块"
            ops_menu = server_dir
            after = _menu_snapshot(server_dir)
            changes.append(
                f"升级目录菜单 id={server_dir.id}: code {before['code']} -> {after['code']}, path {before['path']} -> {after['path']}"
            )
            if verbose:
                print(f"\n[VERBOSE] 菜单 id={server_dir.id} 字段变更")
                _print_field_diff(before, after)

        if not ops_menu:
            ops_menu = Menu(
                name="运维管理",
                code="ops",
                path="/ops",
                icon="Tool",
                type="directory",
                sort_order=2,
                parent_id=None,
                description="运维管理模块",
            )
            session.add(ops_menu)
            await session.flush()
            changes.append(f"创建目录菜单 id={ops_menu.id}: code=ops, path=/ops")

        child_specs = [
            {
                "name": "服务器列表",
                "code": "ops:servers",
                "path": "/ops/servers",
                "icon": "Desktop",
                "type": "menu",
                "sort_order": 1,
                "component": "ops/ServerList",
                "description": "服务器列表管理",
                "legacy_codes": {"server:list"},
                "legacy_paths": {"/server"},
            },
            {
                "name": "执行日志",
                "code": "ops:logs",
                "path": "/ops/logs",
                "icon": "File",
                "type": "menu",
                "sort_order": 4,
                "component": "ops/LogList",
                "description": "任务执行日志",
                "legacy_codes": {"server:logs"},
                "legacy_paths": {"/server/logs"},
            },
        ]

        for spec in child_specs:
            target = by_code.get(spec["code"])

            if not target:
                for m in menus:
                    if (m.code in spec["legacy_codes"]) or (m.path in spec["legacy_paths"] and m.type == "menu"):
                        target = m
                        break

            if target:
                before = _menu_snapshot(target)
                target.name = spec["name"]
                target.code = spec["code"]
                target.path = spec["path"]
                target.icon = spec["icon"]
                target.type = spec["type"]
                target.sort_order = spec["sort_order"]
                target.component = spec["component"]
                target.description = spec["description"]
                target.parent_id = ops_menu.id
                after = _menu_snapshot(target)
                changes.append(
                    f"更新菜单 id={target.id}: code {before['code']} -> {after['code']}, path {before['path']} -> {after['path']}, parent {before['parent_id']} -> {after['parent_id']}"
                )
                if verbose:
                    print(f"\n[VERBOSE] 菜单 id={target.id} 字段变更")
                    _print_field_diff(before, after)
            else:
                target = Menu(
                    name=spec["name"],
                    code=spec["code"],
                    path=spec["path"],
                    icon=spec["icon"],
                    type=spec["type"],
                    sort_order=spec["sort_order"],
                    parent_id=ops_menu.id,
                    component=spec["component"],
                    description=spec["description"],
                )
                session.add(target)
                await session.flush()
                changes.append(
                    f"创建菜单 id={target.id}: code={spec['code']}, path={spec['path']}, parent={ops_menu.id}"
                )
                if verbose:
                    print(f"\n[VERBOSE] 菜单 id={target.id} 字段变更")
                    _print_field_diff({}, _menu_snapshot(target))

        if server_dir and server_dir.id != ops_menu.id:
            children_result = await session.execute(select(Menu).where(Menu.parent_id == server_dir.id))
            server_children = children_result.scalars().all()
            for child in server_children:
                old_parent = child.parent_id
                child.parent_id = ops_menu.id
                changes.append(
                    f"迁移子菜单 id={child.id}: parent {old_parent} -> {ops_menu.id}"
                )
            await session.delete(server_dir)
            changes.append(f"删除 legacy 目录菜单 id={server_dir.id}, code=server")

        _print_changes(changes, dry_run=dry_run)
        if dry_run:
            await session.rollback()
            print("\n[DRY-RUN] 预览完成，未写入数据库")
        else:
            await session.commit()
            print("\n✅ 菜单迁移完成：/server -> /ops（已写入数据库）")

    await engine.dispose()


def parse_args():
    parser = argparse.ArgumentParser(description="迁移 legacy /server 菜单到 /ops")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="执行并写入数据库；默认仅预览(dry-run)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="输出字段级 diff（name/code/path/component）",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(migrate_server_menus_to_ops(dry_run=not args.apply, verbose=args.verbose))
