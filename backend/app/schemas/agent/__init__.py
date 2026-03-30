"""Agent RAG Schemas"""

from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any
from datetime import datetime


# ============ 知识库 ============
class KnowledgeBaseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    embedding_model: str = "default"


class KnowledgeBaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class KnowledgeBaseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    embedding_model: str
    status: bool
    document_count: int = 0
    chunk_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 文档 ============
class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    source: Optional[str] = None
    doc_type: str = "text"


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source: Optional[str] = None


class DocumentResponse(BaseModel):
    id: int
    kb_id: int
    title: str
    content: str
    source: Optional[str] = None
    doc_type: str
    chunk_count: int = 0
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 对话 ============
class ChatRequest(BaseModel):
    kb_id: Optional[int] = None
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1)


class ChatStreamRequest(BaseModel):
    kb_id: Optional[int] = None
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1)


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    kb_id: Optional[int] = None
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List["MessageResponse"] = []

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def extract_messages(cls, obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
            if "messages" not in data or data["messages"] is None:
                data["messages"] = []
            return data
        return obj


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    sources: Optional[List[str]] = None
    tool_calls: Optional[List[dict]] = None
    created_at: datetime

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def extract_data(cls, obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
            return data
        return obj
