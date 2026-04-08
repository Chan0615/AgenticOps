"""Agent RAG API - RAG 核心功能"""

import logging
from typing import Optional

from app.api.agent.rag import router as rag_router

logger = logging.getLogger(__name__)

__all__ = ["rag_router", "reload_rag", "get_rag_instance", "set_rag_instance"]

# ============ 全局 RAG 实例 ============

_rag_instance: Optional[object] = None
_rag_instance_lock = False


def reload_rag():
    """重新加载 RAG 实例（在知识库更新后调用）"""
    global _rag_instance
    _rag_instance = None
    logger.info("RAG 实例已标记为需要重新加载")


def get_rag_instance():
    """获取 RAG 实例"""
    return _rag_instance


def set_rag_instance(instance):
    """设置 RAG 实例"""
    global _rag_instance
    _rag_instance = instance
