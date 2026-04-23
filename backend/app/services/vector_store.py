"""
向量存储服务

负责：
- 调用 Embedding API 生成向量
- 在 pgvector 中存储和检索向量
- 管理文档分块的向量生命周期
"""

import json
import logging
from typing import List, Optional

from app.core.ai import get_ai_config
from app.db import pgvector as pgvector_db

logger = logging.getLogger(__name__)

# Embedding 向量维度
# Qwen text-embedding-v3 = 1024, OpenAI text-embedding-3-small = 1536
EMBEDDING_DIM = 1024


# ============ Embedding 生成 ============


async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    批量生成文本嵌入向量

    使用 OpenAI 兼容的 embedding API（支持 Qwen/DeepSeek/OpenAI）。
    自动分批处理（每批最多 20 条）以避免 API 限制。

    Returns:
        二维数组，每个元素是一个 float 向量
    """
    from openai import AsyncOpenAI

    cfg = get_ai_config()
    if not cfg:
        raise ValueError("未配置 AI 模型，无法生成嵌入向量")

    client = AsyncOpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"],
    )

    # 确定 embedding 模型名
    # 优先使用专用 embedding 模型，否则回退到对话模型的 embedding 变体
    embedding_model = cfg.get("embedding_model")
    if not embedding_model:
        model = cfg.get("model", "")
        if "qwen" in model.lower():
            embedding_model = "text-embedding-v3"
        elif "deepseek" in model.lower():
            embedding_model = "deepseek-chat"  # DeepSeek 用 chat 模型做 embedding
        else:
            embedding_model = "text-embedding-3-small"

    all_embeddings = []
    batch_size = 20

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        # 截断过长的文本（embedding API 通常有 token 限制）
        batch = [t[:8000] if len(t) > 8000 else t for t in batch]

        try:
            response = await client.embeddings.create(
                model=embedding_model,
                input=batch,
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            logger.error(f"Embedding API 调用失败 (batch {i}): {e}")
            # 失败的批次用零向量填充，避免整体失败
            all_embeddings.extend([[0.0] * EMBEDDING_DIM] * len(batch))

    return all_embeddings


async def generate_embedding(text: str) -> List[float]:
    """生成单条文本的嵌入向量"""
    results = await generate_embeddings([text])
    return results[0]


# ============ pgvector 存储操作 ============


async def store_embeddings(
    kb_id: int,
    doc_id: int,
    chunks: List[dict],
) -> int:
    """
    存储文档分块及其向量到 pgvector

    Args:
        kb_id: 知识库 ID
        doc_id: 文档 ID
        chunks: [{"content": "...", "embedding": [...], "chunk_index": 0, "metadata": {}}]

    Returns:
        成功存储的分块数
    """
    pool = await pgvector_db.get_pool()

    async with pool.acquire() as conn:
        # 先删除旧的（同一文档重新索引时）
        await conn.execute(
            "DELETE FROM rag_document_embedding WHERE kb_id = $1 AND doc_id = $2",
            kb_id, doc_id,
        )

        # 批量插入
        count = 0
        for chunk in chunks:
            embedding = chunk["embedding"]
            # pgvector 接受字符串格式的向量 '[1,2,3,...]'
            embedding_str = "[" + ",".join(str(v) for v in embedding) + "]"

            await conn.execute(
                """
                INSERT INTO rag_document_embedding
                    (kb_id, doc_id, chunk_index, content, embedding, metadata)
                VALUES ($1, $2, $3, $4, $5::vector, $6::jsonb)
                """,
                kb_id,
                doc_id,
                chunk.get("chunk_index", count),
                chunk["content"],
                embedding_str,
                json.dumps(chunk.get("metadata", {}), ensure_ascii=False),
            )
            count += 1

    return count


async def delete_doc_embeddings(kb_id: int, doc_id: int):
    """删除文档的所有向量"""
    pool = await pgvector_db.get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM rag_document_embedding WHERE kb_id = $1 AND doc_id = $2",
            kb_id, doc_id,
        )


async def delete_kb_embeddings(kb_id: int):
    """删除知识库的所有向量"""
    pool = await pgvector_db.get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM rag_document_embedding WHERE kb_id = $1",
            kb_id,
        )


async def get_kb_embedding_stats(kb_id: int) -> dict:
    """获取知识库的向量统计"""
    pool = await pgvector_db.get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT
                COUNT(*) AS chunk_count,
                COUNT(DISTINCT doc_id) AS doc_count
            FROM rag_document_embedding
            WHERE kb_id = $1
            """,
            kb_id,
        )
        return {
            "chunk_count": row["chunk_count"] if row else 0,
            "doc_count": row["doc_count"] if row else 0,
        }


# ============ 向量搜索 ============


async def vector_search(
    kb_id: int,
    query_embedding: List[float],
    top_k: int = 5,
    score_threshold: float = 0.3,
) -> List[dict]:
    """
    向量相似度搜索（cosine 距离）

    Returns:
        [{"content": "...", "score": 0.85, "doc_id": 1, "chunk_index": 0, "metadata": {}}]
    """
    pool = await pgvector_db.get_pool()

    embedding_str = "[" + ",".join(str(v) for v in query_embedding) + "]"

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                content,
                doc_id,
                chunk_index,
                metadata,
                1 - (embedding <=> $1::vector) AS score
            FROM rag_document_embedding
            WHERE kb_id = $2
            ORDER BY embedding <=> $1::vector
            LIMIT $3
            """,
            embedding_str, kb_id, top_k,
        )

    results = []
    for row in rows:
        score = float(row["score"])
        if score < score_threshold:
            continue
        results.append({
            "content": row["content"],
            "score": round(score, 4),
            "doc_id": row["doc_id"],
            "chunk_index": row["chunk_index"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
        })

    return results


async def bm25_search(
    kb_id: int,
    query: str,
    top_k: int = 5,
) -> List[dict]:
    """
    BM25 全文检索（基于 PostgreSQL ts_rank）

    使用 'simple' 配置以支持中文分词（逐字拆分）。
    对于更好的中文分词，可考虑安装 zhparser 扩展。

    Returns:
        [{"content": "...", "score": 0.5, "doc_id": 1, "chunk_index": 0, "metadata": {}}]
    """
    pool = await pgvector_db.get_pool()

    # 构建搜索查询：将用户查询拆分为关键词，用 & 连接
    keywords = [w.strip() for w in query.split() if w.strip()]
    if not keywords:
        keywords = [query.strip()]
    # 同时支持每个字拆分（中文场景）
    ts_query_parts = []
    for kw in keywords:
        ts_query_parts.append(kw)
    ts_query_str = " | ".join(ts_query_parts)

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                content,
                doc_id,
                chunk_index,
                metadata,
                ts_rank(
                    to_tsvector('simple', content),
                    to_tsquery('simple', $1)
                ) AS score
            FROM rag_document_embedding
            WHERE kb_id = $2
              AND to_tsvector('simple', content) @@ to_tsquery('simple', $1)
            ORDER BY score DESC
            LIMIT $3
            """,
            ts_query_str, kb_id, top_k,
        )

    results = []
    for row in rows:
        results.append({
            "content": row["content"],
            "score": round(float(row["score"]), 4),
            "doc_id": row["doc_id"],
            "chunk_index": row["chunk_index"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
        })

    return results
