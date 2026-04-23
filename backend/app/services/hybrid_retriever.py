"""
混合检索服务

实现双重召回机制：
1. 向量相似度搜索（语义搜索）—— 捕获语义相关内容
2. BM25 关键词检索（字面匹配）—— 捕获精确关键词匹配

然后通过加权融合算法合并结果，去重排序。
"""

import logging
from typing import List, Optional

from app.services import vector_store

logger = logging.getLogger(__name__)

# 默认权重：向量搜索 0.7，BM25 0.3
DEFAULT_VECTOR_WEIGHT = 0.7
DEFAULT_BM25_WEIGHT = 0.3


async def hybrid_search(
    kb_id: int,
    query: str,
    query_embedding: Optional[List[float]] = None,
    top_k: int = 5,
    vector_weight: float = DEFAULT_VECTOR_WEIGHT,
    bm25_weight: float = DEFAULT_BM25_WEIGHT,
    score_threshold: float = 0.15,
) -> List[dict]:
    """
    混合检索：向量 + BM25 双重召回

    Args:
        kb_id: 知识库 ID
        query: 用户查询文本
        query_embedding: 查询的向量嵌入（如果为 None，自动生成）
        top_k: 返回结果数
        vector_weight: 向量搜索权重（0-1）
        bm25_weight: BM25 搜索权重（0-1）
        score_threshold: 最低分数阈值

    Returns:
        [{"content": "...", "score": 0.85, "doc_id": 1, "chunk_index": 0,
          "metadata": {}, "retrieval_type": "hybrid"}]
    """
    # 1. 生成查询向量（如果未提供）
    if query_embedding is None:
        query_embedding = await vector_store.generate_embedding(query)

    # 2. 并行执行两路检索
    # 扩大检索范围，后续再截断
    fetch_k = top_k * 3

    vector_results = []
    bm25_results = []

    # 向量搜索
    try:
        vector_results = await vector_store.vector_search(
            kb_id=kb_id,
            query_embedding=query_embedding,
            top_k=fetch_k,
            score_threshold=0.1,  # 初始用宽松阈值
        )
        for r in vector_results:
            r["retrieval_type"] = "vector"
    except Exception as e:
        logger.warning(f"向量搜索失败: {e}")

    # BM25 搜索
    try:
        bm25_results = await vector_store.bm25_search(
            kb_id=kb_id,
            query=query,
            top_k=fetch_k,
        )
        for r in bm25_results:
            r["retrieval_type"] = "bm25"
    except Exception as e:
        logger.warning(f"BM25 搜索失败: {e}")

    # 3. 归一化分数
    vector_results = _normalize_scores(vector_results)
    bm25_results = _normalize_scores(bm25_results)

    # 4. 加权融合
    merged = _merge_results(
        vector_results, bm25_results,
        vector_weight=vector_weight,
        bm25_weight=bm25_weight,
    )

    # 5. 过滤低分结果
    merged = [r for r in merged if r["score"] >= score_threshold]

    # 6. 截断到 top_k
    merged = merged[:top_k]

    logger.info(
        f"[Hybrid] kb={kb_id}, query='{query[:30]}...', "
        f"vector={len(vector_results)}, bm25={len(bm25_results)}, "
        f"merged={len(merged)}"
    )

    return merged


def _normalize_scores(results: List[dict]) -> List[dict]:
    """将分数归一化到 [0, 1] 区间"""
    if not results:
        return results

    scores = [r["score"] for r in results]
    max_score = max(scores)
    min_score = min(scores)

    if max_score == min_score:
        for r in results:
            r["score"] = 1.0
        return results

    for r in results:
        r["score"] = (r["score"] - min_score) / (max_score - min_score)

    return results


def _merge_results(
    vector_results: List[dict],
    bm25_results: List[dict],
    vector_weight: float,
    bm25_weight: float,
) -> List[dict]:
    """
    加权融合两路搜索结果

    使用内容文本作为去重 key（同一个 chunk 可能同时被两路召回）。
    """
    # 用 (doc_id, chunk_index) 作为唯一标识
    result_map = {}

    # 处理向量搜索结果
    for r in vector_results:
        key = (r["doc_id"], r["chunk_index"])
        if key not in result_map:
            result_map[key] = {
                "content": r["content"],
                "doc_id": r["doc_id"],
                "chunk_index": r["chunk_index"],
                "metadata": r.get("metadata", {}),
                "vector_score": r["score"],
                "bm25_score": 0.0,
                "retrieval_type": "vector",
            }
        else:
            result_map[key]["vector_score"] = r["score"]

    # 处理 BM25 结果
    for r in bm25_results:
        key = (r["doc_id"], r["chunk_index"])
        if key not in result_map:
            result_map[key] = {
                "content": r["content"],
                "doc_id": r["doc_id"],
                "chunk_index": r["chunk_index"],
                "metadata": r.get("metadata", {}),
                "vector_score": 0.0,
                "bm25_score": r["score"],
                "retrieval_type": "bm25",
            }
        else:
            result_map[key]["bm25_score"] = r["score"]
            result_map[key]["retrieval_type"] = "hybrid"

    # 计算加权总分
    merged = []
    for item in result_map.values():
        item["score"] = round(
            item["vector_score"] * vector_weight + item["bm25_score"] * bm25_weight,
            4,
        )
        merged.append(item)

    # 按总分降序排列
    merged.sort(key=lambda x: x["score"], reverse=True)

    return merged


def format_context(results: List[dict], max_length: int = 4000) -> str:
    """
    将检索结果格式化为 LLM 可用的上下文文本

    Args:
        results: 检索结果列表
        max_length: 最大上下文长度

    Returns:
        格式化的上下文字符串
    """
    if not results:
        return ""

    context_parts = []
    total_len = 0

    for i, r in enumerate(results):
        source = r.get("metadata", {}).get("source", "未知来源")
        score = r.get("score", 0)
        part = f"[资料{i+1}] (来源: {source}, 相关度: {score})\n{r['content']}"

        if total_len + len(part) > max_length:
            break

        context_parts.append(part)
        total_len += len(part)

    return "\n\n---\n\n".join(context_parts)
