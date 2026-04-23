"""智能问数数据模型"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class DataSource(Base):
    """数据源连接配置"""

    __tablename__ = "dq_datasource"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="数据源名称")
    description = Column(String(500), nullable=True, comment="描述")
    db_type = Column(String(20), nullable=False, comment="数据库类型: mysql/postgresql")
    host = Column(String(255), nullable=False, comment="主机地址")
    port = Column(Integer, nullable=False, comment="端口")
    database = Column(String(100), nullable=False, comment="数据库名")
    username = Column(String(100), nullable=False, comment="用户名")
    password_encrypted = Column(String(500), nullable=False, comment="加密后的密码")
    is_system_db = Column(Boolean, default=False, comment="是否为系统自身数据库")
    status = Column(String(20), default="active", comment="状态: active/inactive")
    extra_config = Column(JSON, nullable=True, comment="额外连接参数")
    created_by = Column(String(50), nullable=True, comment="创建人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    table_metadata = relationship(
        "TableMetadata", back_populates="datasource", cascade="all, delete-orphan"
    )
    query_histories = relationship(
        "QueryHistory", back_populates="datasource", cascade="all, delete-orphan"
    )


class TableMetadata(Base):
    """表元数据缓存"""

    __tablename__ = "dq_table_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datasource_id = Column(
        Integer,
        ForeignKey("dq_datasource.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="数据源ID",
    )
    table_name = Column(String(255), nullable=False, comment="表名")
    table_comment = Column(String(500), nullable=True, comment="表注释")
    columns = Column(JSON, nullable=True, comment="字段列表 [{name,type,comment,is_pk,nullable}]")
    sample_data = Column(JSON, nullable=True, comment="样例数据（几行）")
    custom_description = Column(Text, nullable=True, comment="用户自定义表/业务描述")
    synced_at = Column(DateTime, server_default=func.now(), comment="最后同步时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    datasource = relationship("DataSource", back_populates="table_metadata")


class QueryHistory(Base):
    """查询历史"""

    __tablename__ = "dq_query_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datasource_id = Column(
        Integer,
        ForeignKey("dq_datasource.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="数据源ID",
    )
    user_id = Column(
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID",
    )
    question = Column(Text, nullable=False, comment="用户自然语言问题")
    generated_sql = Column(Text, nullable=True, comment="AI 生成的 SQL")
    result_summary = Column(Text, nullable=True, comment="AI 生成的结果摘要")
    result_data = Column(JSON, nullable=True, comment="查询结果数据")
    row_count = Column(Integer, default=0, comment="结果行数")
    execution_time = Column(Float, nullable=True, comment="查询耗时(ms)")
    status = Column(String(20), default="success", comment="状态: success/error")
    error_message = Column(Text, nullable=True, comment="错误信息")
    chart_type = Column(String(20), nullable=True, comment="推荐图表类型: bar/line/pie/table")
    chart_config = Column(JSON, nullable=True, comment="图表配置")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关联关系
    datasource = relationship("DataSource", back_populates="query_histories")
