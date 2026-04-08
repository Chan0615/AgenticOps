"""操作日志数据模型"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    JSON,
)
from sqlalchemy.sql import func
from app.db.database import Base


class OperationLog(Base):
    """操作日志表"""

    __tablename__ = "operation_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, comment="操作用户ID")
    username = Column(String(100), nullable=True, comment="操作用户名")
    module = Column(String(100), nullable=False, comment="操作模块")
    action = Column(String(100), nullable=False, comment="操作类型")
    description = Column(String(500), nullable=True, comment="操作描述")
    method = Column(String(10), nullable=True, comment="HTTP方法")
    path = Column(String(500), nullable=True, comment="请求路径")
    status_code = Column(Integer, nullable=True, comment="响应状态码")
    request_params = Column(JSON, nullable=True, comment="请求参数")
    response_data = Column(JSON, nullable=True, comment="响应数据")
    error_message = Column(Text, nullable=True, comment="错误信息")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(String(500), nullable=True, comment="用户代理")
    execution_time = Column(Integer, nullable=True, comment="执行时间（毫秒）")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
