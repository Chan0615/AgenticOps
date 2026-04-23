"""
多数据源连接管理器

管理多个外部数据库的连接池，支持 MySQL 和 PostgreSQL。
提供安全的查询执行和元数据获取能力。
"""

import asyncio
import base64
import logging
import time
from typing import Any, Dict, List, Optional, Tuple

import aiomysql
from app.core import config

logger = logging.getLogger(__name__)

# 全局连接池缓存 {datasource_id: pool}
_pool_cache: Dict[int, Any] = {}

# ---------- 密码加解密（简单 Base64，生产环境建议 AES） ----------

_ENCRYPT_PREFIX = "b64:"


def encrypt_password(plain: str) -> str:
    """加密密码（Base64 编码，可替换为 AES）"""
    encoded = base64.b64encode(plain.encode("utf-8")).decode("utf-8")
    return f"{_ENCRYPT_PREFIX}{encoded}"


def decrypt_password(encrypted: str) -> str:
    """解密密码"""
    if encrypted.startswith(_ENCRYPT_PREFIX):
        encoded = encrypted[len(_ENCRYPT_PREFIX):]
        return base64.b64decode(encoded.encode("utf-8")).decode("utf-8")
    # 兼容未加密的旧数据
    return encrypted


# ---------- 连接池管理 ----------


async def _create_mysql_pool(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    **kwargs,
) -> aiomysql.Pool:
    """创建 MySQL 连接池"""
    pool = await aiomysql.create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        db=database,
        charset="utf8mb4",
        autocommit=True,
        minsize=1,
        maxsize=5,
        connect_timeout=10,
        **kwargs,
    )
    return pool


async def get_pool(datasource) -> Any:
    """获取或创建数据源连接池"""
    ds_id = datasource.id if hasattr(datasource, "id") else id(datasource)

    if ds_id in _pool_cache:
        pool = _pool_cache[ds_id]
        # 简单存活检测
        if pool is not None:
            try:
                if hasattr(pool, "size") and pool.size > 0:
                    return pool
            except Exception:
                pass
            # 池不可用，清理后重建
            try:
                pool.close()
                await pool.wait_closed()
            except Exception:
                pass
            del _pool_cache[ds_id]

    password = decrypt_password(datasource.password_encrypted)
    db_type = datasource.db_type.lower()

    if db_type == "mysql":
        pool = await _create_mysql_pool(
            host=datasource.host,
            port=datasource.port,
            user=datasource.username,
            password=password,
            database=datasource.database,
        )
    elif db_type == "postgresql":
        # PostgreSQL 支持（需要 asyncpg）
        try:
            import asyncpg

            pool = await asyncpg.create_pool(
                host=datasource.host,
                port=datasource.port,
                user=datasource.username,
                password=password,
                database=datasource.database,
                min_size=1,
                max_size=5,
                timeout=10,
            )
        except ImportError:
            raise RuntimeError(
                "PostgreSQL 支持需要安装 asyncpg: pip install asyncpg"
            )
    else:
        raise ValueError(f"不支持的数据库类型: {db_type}")

    _pool_cache[ds_id] = pool
    return pool


async def close_pool(datasource_id: int):
    """关闭指定数据源的连接池"""
    pool = _pool_cache.pop(datasource_id, None)
    if pool is None:
        return
    try:
        if hasattr(pool, "close"):
            pool.close()
            if hasattr(pool, "wait_closed"):
                await pool.wait_closed()
        elif hasattr(pool, "terminate"):
            await pool.terminate()
    except Exception as e:
        logger.warning(f"关闭连接池 {datasource_id} 失败: {e}")


async def close_all_pools():
    """关闭所有连接池"""
    for ds_id in list(_pool_cache.keys()):
        await close_pool(ds_id)


# ---------- 测试连接 ----------


async def test_connection(
    db_type: str,
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
) -> dict:
    """测试数据库连接"""
    db_type = db_type.lower()
    start = time.time()
    try:
        if db_type == "mysql":
            conn = await aiomysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                db=database,
                charset="utf8mb4",
                connect_timeout=10,
            )
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
                await cur.fetchone()
            conn.close()
        elif db_type == "postgresql":
            try:
                import asyncpg

                conn = await asyncpg.connect(
                    host=host,
                    port=port,
                    user=username,
                    password=password,
                    database=database,
                    timeout=10,
                )
                await conn.fetchval("SELECT 1")
                await conn.close()
            except ImportError:
                return {"success": False, "message": "需要安装 asyncpg"}
        else:
            return {"success": False, "message": f"不支持的数据库类型: {db_type}"}

        elapsed = round((time.time() - start) * 1000, 1)
        return {"success": True, "message": f"连接成功 ({elapsed}ms)"}
    except Exception as e:
        return {"success": False, "message": f"连接失败: {str(e)}"}


# ---------- 执行查询 ----------


async def execute_query(
    datasource,
    sql: str,
    params: Optional[tuple] = None,
    timeout: int = 30,
) -> dict:
    """
    在指定数据源上执行 SQL 查询

    Returns:
        {
            "columns": ["col1", "col2", ...],
            "rows": [[val1, val2, ...], ...],
            "row_count": int,
            "execution_time": float (ms),
        }
    """
    pool = await get_pool(datasource)
    db_type = datasource.db_type.lower()
    start = time.time()

    try:
        if db_type == "mysql":
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await asyncio.wait_for(
                        cur.execute(sql, params), timeout=timeout
                    )
                    rows = await cur.fetchall()
                    columns = [desc[0] for desc in cur.description] if cur.description else []
        elif db_type == "postgresql":
            async with pool.acquire() as conn:
                records = await asyncio.wait_for(
                    conn.fetch(sql, *(params or ())), timeout=timeout
                )
                columns = list(records[0].keys()) if records else []
                rows = [dict(r) for r in records]
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")

        elapsed = round((time.time() - start) * 1000, 1)

        # 统一转为 list[dict] 格式
        if db_type == "mysql":
            data = [dict(row) for row in rows]
        else:
            data = rows

        # 处理不可序列化的值
        for row in data:
            for key, val in row.items():
                if isinstance(val, bytes):
                    row[key] = val.decode("utf-8", errors="replace")
                elif hasattr(val, "isoformat"):
                    row[key] = val.isoformat()
                elif val is None:
                    pass
                elif not isinstance(val, (str, int, float, bool)):
                    row[key] = str(val)

        return {
            "columns": columns,
            "rows": data,
            "row_count": len(data),
            "execution_time": elapsed,
        }
    except asyncio.TimeoutError:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "execution_time": round((time.time() - start) * 1000, 1),
            "error": f"查询超时（{timeout}秒）",
        }
    except Exception as e:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "execution_time": round((time.time() - start) * 1000, 1),
            "error": str(e),
        }


# ---------- 获取表元数据 ----------


async def fetch_table_metadata(datasource) -> List[dict]:
    """
    从数据源获取所有表的元数据（表名、注释、字段信息）

    Returns:
        [
            {
                "table_name": "xxx",
                "table_comment": "...",
                "columns": [
                    {"name": "id", "type": "int", "comment": "主键", "is_pk": True, "nullable": False},
                    ...
                ]
            },
            ...
        ]
    """
    pool = await get_pool(datasource)
    db_type = datasource.db_type.lower()
    tables = []

    if db_type == "mysql":
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 获取所有表
                await cur.execute(
                    "SELECT TABLE_NAME, TABLE_COMMENT "
                    "FROM INFORMATION_SCHEMA.TABLES "
                    "WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE' "
                    "ORDER BY TABLE_NAME",
                    (datasource.database,),
                )
                table_rows = await cur.fetchall()

                for tr in table_rows:
                    table_name = tr["TABLE_NAME"]
                    table_comment = tr.get("TABLE_COMMENT", "")

                    # 获取字段信息
                    await cur.execute(
                        "SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT, "
                        "COLUMN_KEY, IS_NULLABLE "
                        "FROM INFORMATION_SCHEMA.COLUMNS "
                        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s "
                        "ORDER BY ORDINAL_POSITION",
                        (datasource.database, table_name),
                    )
                    col_rows = await cur.fetchall()
                    columns = [
                        {
                            "name": c["COLUMN_NAME"],
                            "type": c["COLUMN_TYPE"],
                            "comment": c.get("COLUMN_COMMENT", ""),
                            "is_pk": c.get("COLUMN_KEY") == "PRI",
                            "nullable": c.get("IS_NULLABLE") == "YES",
                        }
                        for c in col_rows
                    ]

                    tables.append(
                        {
                            "table_name": table_name,
                            "table_comment": table_comment,
                            "columns": columns,
                        }
                    )

    elif db_type == "postgresql":
        async with pool.acquire() as conn:
            # 获取所有表
            table_rows = await conn.fetch(
                "SELECT c.relname AS table_name, "
                "pg_catalog.obj_description(c.oid) AS table_comment "
                "FROM pg_catalog.pg_class c "
                "JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace "
                "WHERE n.nspname = 'public' AND c.relkind = 'r' "
                "ORDER BY c.relname"
            )

            for tr in table_rows:
                table_name = tr["table_name"]
                table_comment = tr.get("table_comment", "")

                col_rows = await conn.fetch(
                    "SELECT a.attname AS column_name, "
                    "pg_catalog.format_type(a.atttypid, a.atttypmod) AS column_type, "
                    "pg_catalog.col_description(a.attrelid, a.attnum) AS column_comment, "
                    "CASE WHEN pk.contype = 'p' THEN true ELSE false END AS is_pk, "
                    "NOT a.attnotnull AS nullable "
                    "FROM pg_catalog.pg_attribute a "
                    "LEFT JOIN pg_catalog.pg_constraint pk ON "
                    "  pk.conrelid = a.attrelid AND a.attnum = ANY(pk.conkey) AND pk.contype = 'p' "
                    "WHERE a.attrelid = $1::regclass AND a.attnum > 0 AND NOT a.attisdropped "
                    "ORDER BY a.attnum",
                    table_name,
                )
                columns = [
                    {
                        "name": c["column_name"],
                        "type": c["column_type"],
                        "comment": c.get("column_comment", "") or "",
                        "is_pk": c.get("is_pk", False),
                        "nullable": c.get("nullable", True),
                    }
                    for c in col_rows
                ]

                tables.append(
                    {
                        "table_name": table_name,
                        "table_comment": table_comment or "",
                        "columns": columns,
                    }
                )

    return tables


async def fetch_sample_data(
    datasource, table_name: str, limit: int = 3
) -> List[dict]:
    """获取表的样例数据"""
    db_type = datasource.db_type.lower()
    # 防注入：只允许字母、数字、下划线
    import re
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_name):
        return []

    if db_type == "mysql":
        sql = f"SELECT * FROM `{table_name}` LIMIT {limit}"
    elif db_type == "postgresql":
        sql = f'SELECT * FROM "{table_name}" LIMIT {limit}'
    else:
        return []

    result = await execute_query(datasource, sql, timeout=10)
    return result.get("rows", [])
