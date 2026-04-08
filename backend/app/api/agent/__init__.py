"""Agent RAG API - 统一的 RAG 知识库和智能对话模块"""

import logging
from typing import Optional

from app.api.agent.rag import router as rag_router

logger = logging.getLogger(__name__)

__all__ = ["rag_router"]
