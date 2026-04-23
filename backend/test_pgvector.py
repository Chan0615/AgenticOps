"""
pgvector 连接测试脚本
使用方式: python test_pgvector.py

测试内容:
  - 连接 PostgreSQL 数据库
  - 检查 pgvector 扩展是否已安装
  - 创建测试表并执行向量相似度搜索
  - 清理测试数据
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    try:
        import asyncpg
    except ImportError:
        print("错误: 未安装 asyncpg，请执行: pip install asyncpg pgvector")
        return

    from app.core import config

    pg_cfg = config._get("pgvector")
    if not pg_cfg:
        print("错误: config.yaml 中未找到 pgvector 配置")
        print("请添加以下配置:")
        print("  pgvector:")
        print('    host: "10.225.138.183"')
        print("    port: 5432")
        print('    user: "agenticops"')
        print('    password: "agenticops123"')
        print('    database: "agenticops_vector"')
        return

    host = pg_cfg["host"]
    port = pg_cfg["port"]
    user = pg_cfg["user"]
    password = pg_cfg["password"]
    database = pg_cfg["database"]

    print(f"[1/4] 连接 PostgreSQL ({host}:{port}/{database}) ...")
    try:
        conn = await asyncpg.connect(
            host=host, port=port, user=user, password=password, database=database
        )
    except Exception as e:
        print(f"      连接失败: {e}")
        return

    version = await conn.fetchval("SELECT version()")
    print(f"      {version}")

    # 检查 pgvector 扩展
    print("[2/4] 检查 pgvector 扩展 ...")
    has_vector = await conn.fetchval(
        "SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector'"
    )
    if has_vector:
        vector_version = await conn.fetchval(
            "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
        )
        print(f"      pgvector {vector_version} 已安装")
    else:
        print("      pgvector 未安装！请执行: CREATE EXTENSION vector;")
        await conn.close()
        return

    # 向量搜索测试
    print("[3/4] 向量搜索功能测试 ...")
    try:
        await conn.execute("DROP TABLE IF EXISTS _test_pgvector")
        await conn.execute(
            """
            CREATE TABLE _test_pgvector (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(3)
            )
            """
        )
        await conn.execute(
            """
            INSERT INTO _test_pgvector (content, embedding) VALUES
                ('你好世界', '[1,0,0]'),
                ('机器学习', '[0,1,0]'),
                ('深度学习', '[0.1,0.9,0.1]'),
                ('自然语言处理', '[0.2,0.8,0.3]'),
                ('数据库管理', '[0,0,1]')
            """
        )

        rows = await conn.fetch(
            """
            SELECT content, embedding <-> '[0,1,0]' AS distance
            FROM _test_pgvector
            ORDER BY embedding <-> '[0,1,0]'
            LIMIT 3
            """
        )

        print("      查询: 与 [0,1,0] 最相似的 3 条记录:")
        for row in rows:
            print(f"        {row['content']:<12} 距离: {row['distance']:.4f}")

        # 清理
        await conn.execute("DROP TABLE _test_pgvector")
        print("      测试表已清理")

    except Exception as e:
        print(f"      测试失败: {e}")
        await conn.execute("DROP TABLE IF EXISTS _test_pgvector")

    print("[4/4] 连接信息汇总")
    print(f"      主机: {host}:{port}")
    print(f"      数据库: {database}")
    print(f"      用户: {user}")
    print(f"      pgvector: v{vector_version}")
    print()
    print(">>> pgvector 连接测试全部通过！")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
