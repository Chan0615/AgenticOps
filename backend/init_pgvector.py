"""
pgvector 向量表初始化脚本
使用方式: python init_pgvector.py

功能:
  - 连接 PostgreSQL (pgvector)
  - 创建 vector 扩展
  - 创建 rag_document_embedding 表及索引
  - 幂等操作，可重复运行
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    from app.db.pgvector import init_tables, get_pool, close_pool

    print("[1/2] 初始化 pgvector 向量表 ...")
    try:
        await init_tables()
        print("      向量表创建完成")
    except Exception as e:
        print(f"      初始化失败: {e}")
        return

    print("[2/2] 验证表结构 ...")
    pool = await get_pool()
    async with pool.acquire() as conn:
        # 检查表
        row = await conn.fetchrow(
            "SELECT COUNT(*) AS cnt FROM information_schema.tables "
            "WHERE table_name = 'rag_document_embedding'"
        )
        print(f"      rag_document_embedding 表: {'存在' if row['cnt'] > 0 else '不存在'}")

        # 检查列
        cols = await conn.fetch(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_name = 'rag_document_embedding' ORDER BY ordinal_position"
        )
        print(f"      字段数: {len(cols)}")
        for c in cols:
            print(f"        - {c['column_name']}: {c['data_type']}")

        # 检查索引
        idxs = await conn.fetch(
            "SELECT indexname FROM pg_indexes WHERE tablename = 'rag_document_embedding'"
        )
        print(f"      索引数: {len(idxs)}")
        for idx in idxs:
            print(f"        - {idx['indexname']}")

    await close_pool()
    print("\n>>> pgvector 初始化完成！")


if __name__ == "__main__":
    asyncio.run(main())
