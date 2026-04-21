"""Agent RAG API - 统一的 RAG 知识库和智能对话模块"""

import logging
from typing import Optional

from app.api.agent.rag import router as rag_router
from app.api.agent.system_chat import router as system_chat_router

logger = logging.getLogger(__name__)

__all__ = ["rag_router", "system_chat_router"]
