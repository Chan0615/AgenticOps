"""
PostgreSQL + pgvector 连接管理

提供异步连接池，用于 RAG 知识库的向量存储和检索。
与主 MySQL 数据库独立，使用 asyncpg 直接连接。
"""

import logging
from typing import Optional

import asyncpg

from app.core import config

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.Pool] = None


def _get_pgvector_config() -> dict:
    """获取 pgvector 配置"""
    cfg = config._get("pgvector")
    if not cfg:
        raise RuntimeError(
            "pgvector 未配置。请在 config.yaml 中添加 pgvector 段。\n"
            "参考 PGVECTOR_INSTALL.md 部署 PostgreSQL + pgvector。"
        )
    return cfg


async def get_pool() -> asyncpg.Pool:
    """获取或创建 pgvector 连接池"""
    global _pool
    if _pool is not None and not _pool._closed:
        return _pool

    cfg = _get_pgvector_config()
    _pool = await asyncpg.create_pool(
        host=cfg["host"],
        port=cfg.get("port", 5432),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        min_size=2,
        max_size=10,
        timeout=15,
    )
    logger.info(f"pgvector 连接池已创建: {cfg['host']}:{cfg.get('port', 5432)}/{cfg['database']}")
    return _pool


async def get_conn():
    """获取一个连接（用于 async with）"""
    pool = await get_pool()
    return pool.acquire()


async def close_pool():
    """关闭连接池"""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("pgvector 连接池已关闭")


async def init_tables():
    """
    初始化 pgvector 向量表（幂等操作）

    创建:
    - rag_document_embedding: 文档分块的向量嵌入存储
    """
    pool = await get_pool()

    async with pool.acquire() as conn:
        # 确保 vector 扩展已启用
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # 创建向量表
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS rag_document_embedding (
                id          BIGSERIAL PRIMARY KEY,
                kb_id       INTEGER NOT NULL,
                doc_id      INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL DEFAULT 0,
                content     TEXT NOT NULL,
                embedding   vector(1024),
                metadata    JSONB DEFAULT '{}',
                created_at  TIMESTAMPTZ DEFAULT NOW()
            )
        """)

        # 创建索引
        # IVFFlat 索引：适合中等规模数据（< 100 万行），需要先有数据才能 build
        # 先创建普通索引，数据量大了再切换 IVFFlat/HNSW
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_rag_emb_kb_id
            ON rag_document_embedding (kb_id)
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_rag_emb_doc_id
            ON rag_document_embedding (doc_id)
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_rag_emb_kb_doc
            ON rag_document_embedding (kb_id, doc_id)
        """)

        # HNSW 向量索引（cosine 距离）—— 数据量少时自动跳过
        row_count = await conn.fetchval(
            "SELECT COUNT(*) FROM rag_document_embedding"
        )
        if row_count > 0:
            # 检查索引是否已存在
            idx_exists = await conn.fetchval(
                "SELECT COUNT(*) FROM pg_indexes WHERE indexname = 'idx_rag_emb_hnsw'"
            )
            if not idx_exists:
                await conn.execute("""
                    CREATE INDEX idx_rag_emb_hnsw
                    ON rag_document_embedding
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 64)
                """)

        # 全文搜索索引（BM25 用）
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_rag_emb_content_gin
            ON rag_document_embedding
            USING gin (to_tsvector('simple', content))
        """)

    logger.info("pgvector 向量表初始化完成")
