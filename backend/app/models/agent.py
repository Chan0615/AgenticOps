"""Agent RAG 数据模型"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class KnowledgeBase(Base):
    """知识库"""

    __tablename__ = "agent_knowledge_base"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="知识库名称")
    description = Column(Text, nullable=True, comment="描述")
    embedding_model = Column(String(100), default="default", comment="嵌入模型")
    status = Column(Boolean, default=True, comment="状态")
    document_count = Column(Integer, default=0, comment="文档数量")
    chunk_count = Column(Integer, default=0, comment="分块数量")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    documents = relationship(
        "Document", back_populates="knowledge_base", cascade="all, delete-orphan"
    )


class Document(Base):
    """知识文档"""

    __tablename__ = "agent_document"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kb_id = Column(
        Integer,
        ForeignKey("agent_knowledge_base.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(255), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="原文内容")
    source = Column(String(255), nullable=True, comment="来源")
    doc_type = Column(String(50), default="text", comment="类型: text/markdown/pdf")
    chunk_count = Column(Integer, default=0, comment="分块数")
    status = Column(Boolean, default=True, comment="状态: 待处理/已索引")
    meta_info = Column(JSON, nullable=True, comment="元信息")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    knowledge_base = relationship("KnowledgeBase", back_populates="documents")
    chunks = relationship(
        "DocumentChunk", back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    """文档分块"""

    __tablename__ = "agent_document_chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(
        Integer, ForeignKey("agent_document.id", ondelete="CASCADE"), nullable=False
    )
    kb_id = Column(
        Integer,
        ForeignKey("agent_knowledge_base.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index = Column(Integer, default=0, comment="分块序号")
    content = Column(Text, nullable=False, comment="分块内容")
    embedding = Column(JSON, nullable=True, comment="向量（JSON 数组）")
    meta_info = Column(JSON, nullable=True, comment="元信息")
    created_at = Column(DateTime, server_default=func.now())

    document = relationship("Document", back_populates="chunks")


class Conversation(Base):
    """对话记录"""

    __tablename__ = "agent_conversation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False
    )
    kb_id = Column(
        Integer,
        ForeignKey("agent_knowledge_base.id", ondelete="SET NULL"),
        nullable=True,
    )
    title = Column(String(255), default="新对话", comment="标题")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    messages = relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ConversationMessage.id",
    )


class ConversationMessage(Base):
    """对话消息"""

    __tablename__ = "agent_conversation_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(
        Integer, ForeignKey("agent_conversation.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String(20), nullable=False, comment="user/assistant/system")
    content = Column(Text, nullable=False, comment="消息内容")
    sources = Column(JSON, nullable=True, comment="引用来源")
    tool_calls = Column(JSON, nullable=True, comment="Agent 工具调用记录")
    created_at = Column(DateTime, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
