"""服务器管理数据模型"""

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


class ServerGroup(Base):
    """服务器分组"""

    __tablename__ = "server_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="分组名称")
    description = Column(Text, nullable=True, comment="描述")
    environment = Column(String(50), comment="环境: fuchunyun/aliyun/binjiang/aliyunyc")
    status = Column(Boolean, default=True, comment="状态")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    servers = relationship("Server", back_populates="group", cascade="all, delete-orphan")


class Server(Base):
    """服务器"""

    __tablename__ = "server"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(
        Integer, ForeignKey("server_group.id", ondelete="SET NULL"), nullable=True
    )
    name = Column(String(100), nullable=False, comment="服务器名称")
    hostname = Column(String(255), nullable=False, comment="主机名/IP")
    port = Column(Integer, default=22, comment="SSH 端口")
    username = Column(String(100), nullable=False, comment="SSH 用户名")
    password = Column(String(500), nullable=True, comment="SSH 密码（加密存储）")
    private_key = Column(Text, nullable=True, comment="SSH 私钥")
    os_type = Column(String(50), default="linux", comment="操作系统类型")
    tags = Column(JSON, nullable=True, comment="标签")
    status = Column(Boolean, default=True, comment="状态")
    salt_minion_id = Column(String(255), nullable=True, comment="Salt Minion ID")
    last_connected_at = Column(DateTime, nullable=True, comment="最后连接时间")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    group = relationship("ServerGroup", back_populates="servers")
