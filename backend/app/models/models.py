from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    """用户模型"""

    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(
        String(50), unique=True, index=True, nullable=False, comment="用户名"
    )
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    full_name = Column(String(100), nullable=True, comment="真实姓名")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    status = Column(Boolean, default=True, comment="状态：0-禁用，1-正常")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    roles = relationship(
        "UserRole", back_populates="user", cascade="all, delete-orphan"
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


class Role(Base):
    """角色模型"""

    __tablename__ = "sys_role"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(
        String(50), unique=True, index=True, nullable=False, comment="角色名称"
    )
    code = Column(
        String(50), unique=True, index=True, nullable=False, comment="角色代码"
    )
    description = Column(String(255), nullable=True, comment="描述")
    status = Column(Boolean, default=True, comment="状态：0-禁用，1-正常")
    sort_order = Column(Integer, default=0, comment="排序")
    permissions = relationship(
        "RoleMenu", back_populates="role", cascade="all, delete-orphan"
    )
    users = relationship(
        "UserRole", back_populates="role", cascade="all, delete-orphan"
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


class UserRole(Base):
    """用户角色关联表"""

    __tablename__ = "sys_user_role"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False
    )
    role_id = Column(
        Integer, ForeignKey("sys_role.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Menu(Base):
    """菜单模型"""

    __tablename__ = "sys_menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="菜单名称")
    code = Column(
        String(50), unique=True, index=True, nullable=False, comment="菜单代码"
    )
    path = Column(String(255), nullable=True, comment="路由路径")
    component = Column(String(255), nullable=True, comment="组件路径")
    icon = Column(String(50), nullable=True, comment="图标")
    parent_id = Column(
        Integer,
        ForeignKey("sys_menu.id", ondelete="CASCADE"),
        nullable=True,
        comment="父菜单ID",
    )
    sort_order = Column(Integer, default=0, comment="排序")
    type = Column(String(20), default="menu", comment="类型：menu/directory/button")
    status = Column(Boolean, default=True, comment="状态：0-禁用，1-正常")
    meta = Column(JSON, nullable=True, comment="元数据")
    description = Column(String(255), nullable=True, comment="描述")
    roles = relationship(
        "RoleMenu", back_populates="menu", cascade="all, delete-orphan"
    )
    children = relationship(
        "Menu", backref="parent", remote_side=[id], cascade="save-update, merge"
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


class RoleMenu(Base):
    """角色菜单关联表"""

    __tablename__ = "sys_role_menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(
        Integer, ForeignKey("sys_role.id", ondelete="CASCADE"), nullable=False
    )
    menu_id = Column(
        Integer, ForeignKey("sys_menu.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    role = relationship("Role", back_populates="permissions")
    menu = relationship("Menu", back_populates="roles")


class KnowledgeDocument(Base):
    """知识库文档模型"""

    __tablename__ = "knowledge_document"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="文档名称")
    description = Column(Text, nullable=True, comment="文档描述")
    file_path = Column(String(500), nullable=False, comment="文件存储路径")
    file_type = Column(String(50), nullable=False, comment="文件类型: txt/pdf/docx/md")
    file_size = Column(Integer, nullable=False, comment="文件大小(字节)")
    status = Column(String(20), default="pending", comment="状态: pending/indexed/error")
    chunk_count = Column(Integer, default=0, comment="分片数量")
    error_msg = Column(Text, nullable=True, comment="错误信息")
    created_by = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="创建者")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    creator = relationship("User")


class DocumentChunk(Base):
    """文档分片模型"""

    __tablename__ = "document_chunk"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("knowledge_document.id", ondelete="CASCADE"), nullable=False, comment="所属文档ID")
    content = Column(Text, nullable=False, comment="分片内容")
    chunk_index = Column(Integer, nullable=False, comment="分片序号")
    char_count = Column(Integer, nullable=False, comment="字符数")
    faiss_id = Column(Integer, nullable=True, comment="FAISS向量ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    document = relationship("KnowledgeDocument", back_populates="chunks")


# ============================================================
# Agent RAG 模块模型（可选，需要时取消注释）
# ============================================================
# 如果需要使用 Agent 功能，请取消以下导入注释：
# from app.models.agent import (
#     KnowledgeBase,
#     Document,
#     DocumentChunk as AgentDocumentChunk,
#     Conversation,
#     ConversationMessage
# )
