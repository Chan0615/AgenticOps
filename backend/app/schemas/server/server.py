"""服务器相关 Schema（Ops 模块）"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ServerBase(BaseModel):
    """服务器基础 Schema"""
    name: str = Field(..., description="服务器名称", max_length=100)
    hostname: str = Field(..., description="IP地址或域名", max_length=255)
    port: int = Field(default=22, description="SSH端口", ge=1, le=65535)
    username: str = Field(default="root", description="登录用户名", max_length=50)
    salt_minion_id: Optional[str] = Field(None, description="Salt Minion ID", max_length=100)
    environment: str = Field(default="production", description="环境: production/staging/testing")
    tags: Optional[List[str]] = Field(default=None, description="标签列表")
    description: Optional[str] = Field(None, description="描述", max_length=500)


class ServerCreate(ServerBase):
    """创建服务器 Schema"""
    pass


class ServerUpdate(BaseModel):
    """更新服务器 Schema"""
    name: Optional[str] = Field(None, description="服务器名称", max_length=100)
    hostname: Optional[str] = Field(None, description="IP地址或域名", max_length=255)
    port: Optional[int] = Field(None, description="SSH端口", ge=1, le=65535)
    username: Optional[str] = Field(None, description="登录用户名", max_length=50)
    salt_minion_id: Optional[str] = Field(None, description="Salt Minion ID", max_length=100)
    environment: Optional[str] = Field(None, description="环境: production/staging/testing")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    status: Optional[str] = Field(None, description="状态: online/offline/unknown")
    description: Optional[str] = Field(None, description="描述", max_length=500)


class ServerResponse(ServerBase):
    """服务器响应 Schema"""
    id: int
    status: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServerListResponse(BaseModel):
    """服务器列表响应"""
    code: int = 200
    message: str = "success"
    data: List[ServerResponse]
    total: int


class ConnectionTestRequest(BaseModel):
    """连接测试请求"""
    server_id: int = Field(..., description="服务器ID")
    test_type: str = Field(default="salt", description="测试类型: salt/jumpserver")
