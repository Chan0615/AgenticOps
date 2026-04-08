"""服务器管理 Schema"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============ 服务器分组 Schema ============

class ServerGroupBase(BaseModel):
    name: str = Field(..., description="分组名称")
    environment: str = Field(..., description="环境标识")
    description: Optional[str] = Field(None, description="描述")


class ServerGroupCreate(ServerGroupBase):
    pass


class ServerGroupResponse(ServerGroupBase):
    id: int
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 服务器 Schema ============

class ServerBase(BaseModel):
    name: str = Field(..., description="服务器名称")
    hostname: str = Field(..., description="主机名/IP")
    port: int = Field(default=22, description="SSH端口")
    username: str = Field(..., description="SSH用户名")
    os_type: str = Field(default="linux", description="操作系统类型")
    group_id: Optional[int] = Field(None, description="分组ID")
    salt_minion_id: Optional[str] = Field(None, description="Salt Minion ID")
    tags: Optional[dict] = Field(None, description="标签")


class ServerCreate(ServerBase):
    password: Optional[str] = Field(None, description="SSH密码")
    private_key: Optional[str] = Field(None, description="SSH私钥")


class ServerUpdate(BaseModel):
    name: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None
    os_type: Optional[str] = None
    group_id: Optional[int] = None
    salt_minion_id: Optional[str] = None
    tags: Optional[dict] = None
    status: Optional[bool] = None


class ServerResponse(ServerBase):
    id: int
    status: bool
    last_connected_at: Optional[datetime] = None
    is_connected: Optional[bool] = Field(None, description="当前是否连通")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServerListResponse(BaseModel):
    """服务器列表响应（包含分页信息）"""
    total: int
    items: list[ServerResponse]


# ============ 连通性检测 Schema ============

class ConnectivityCheckResponse(BaseModel):
    server_id: int
    hostname: str
    is_connected: bool
    response_time: Optional[float] = None
    error_message: Optional[str] = None


# ============ 操作日志 Schema ============

class OperationLogBase(BaseModel):
    module: str
    action: str
    description: Optional[str] = None


class OperationLogResponse(OperationLogBase):
    id: int
    user_id: Optional[int] = None
    username: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    status_code: Optional[int] = None
    request_params: Optional[dict] = None
    response_data: Optional[dict] = None
    error_message: Optional[str] = None
    ip_address: Optional[str] = None
    execution_time: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OperationLogListResponse(BaseModel):
    """操作日志列表响应"""
    total: int
    items: list[OperationLogResponse]
