"""智能问数相关 Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


# ============ 数据源 Schema ============


class DataSourceBase(BaseModel):
    """数据源基础 Schema"""
    name: str = Field(..., description="数据源名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    db_type: str = Field(..., description="数据库类型: mysql/postgresql")
    host: str = Field(..., description="主机地址", max_length=255)
    port: int = Field(..., description="端口", ge=1, le=65535)
    database: str = Field(..., description="数据库名", max_length=100)
    username: str = Field(..., description="用户名", max_length=100)
    is_system_db: bool = Field(default=False, description="是否为系统自身数据库")
    extra_config: Optional[dict] = Field(None, description="额外连接参数")


class DataSourceCreate(DataSourceBase):
    """创建数据源 Schema"""
    password: str = Field(..., description="密码", max_length=255)


class DataSourceUpdate(BaseModel):
    """更新数据源 Schema"""
    name: Optional[str] = Field(None, description="数据源名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    db_type: Optional[str] = Field(None, description="数据库类型")
    host: Optional[str] = Field(None, description="主机地址", max_length=255)
    port: Optional[int] = Field(None, description="端口", ge=1, le=65535)
    database: Optional[str] = Field(None, description="数据库名", max_length=100)
    username: Optional[str] = Field(None, description="用户名", max_length=100)
    password: Optional[str] = Field(None, description="密码", max_length=255)
    status: Optional[str] = Field(None, description="状态: active/inactive")
    extra_config: Optional[dict] = Field(None, description="额外连接参数")


class DataSourceResponse(BaseModel):
    """数据源响应 Schema"""
    id: int
    name: str
    description: Optional[str] = None
    db_type: str
    host: str
    port: int
    database: str
    username: str
    is_system_db: bool
    status: str
    extra_config: Optional[dict] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DataSourceListResponse(BaseModel):
    """数据源列表响应"""
    code: int = 200
    message: str = "success"
    data: List[DataSourceResponse]
    total: int


class DataSourceTestRequest(BaseModel):
    """测试连接请求（不通过已保存的数据源，直接测试）"""
    db_type: str = Field(..., description="数据库类型: mysql/postgresql")
    host: str = Field(..., description="主机地址")
    port: int = Field(..., description="端口")
    database: str = Field(..., description="数据库名")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


# ============ 表元数据 Schema ============


class ColumnInfo(BaseModel):
    """字段信息"""
    name: str
    type: str
    comment: Optional[str] = None
    is_pk: bool = False
    nullable: bool = True


class TableMetadataResponse(BaseModel):
    """表元数据响应"""
    id: int
    datasource_id: int
    table_name: str
    table_comment: Optional[str] = None
    columns: Optional[List[ColumnInfo]] = None
    sample_data: Optional[List[dict]] = None
    custom_description: Optional[str] = None
    synced_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TableDescriptionUpdate(BaseModel):
    """更新表描述"""
    custom_description: str = Field(..., description="自定义表描述")


# ============ 智能问数 Schema ============


class QueryAskRequest(BaseModel):
    """智能问数请求"""
    datasource_id: int = Field(..., description="数据源ID")
    question: str = Field(..., description="自然语言问题")
    conversation_history: Optional[List[dict]] = Field(
        None, description="对话历史 [{role, content}]"
    )


class QueryAskResponse(BaseModel):
    """智能问数响应"""
    history_id: int
    question: str
    generated_sql: str
    result_data: Optional[List[dict]] = None
    result_summary: Optional[str] = None
    row_count: int = 0
    execution_time: Optional[float] = None
    chart_type: Optional[str] = None
    chart_config: Optional[dict] = None
    status: str = "success"
    error_message: Optional[str] = None


class QueryHistoryResponse(BaseModel):
    """查询历史响应"""
    id: int
    datasource_id: int
    question: str
    generated_sql: Optional[str] = None
    result_summary: Optional[str] = None
    row_count: int = 0
    execution_time: Optional[float] = None
    status: str
    chart_type: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class QueryHistoryListResponse(BaseModel):
    """查询历史列表响应"""
    code: int = 200
    message: str = "success"
    data: List[QueryHistoryResponse]
    total: int


class QueryHistoryDetailResponse(QueryHistoryResponse):
    """查询历史详情（包含结果数据）"""
    result_data: Optional[List[dict]] = None
    chart_config: Optional[dict] = None
