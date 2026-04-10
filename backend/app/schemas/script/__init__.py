"""脚本相关 Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ScriptBase(BaseModel):
    """脚本基础 Schema"""
    name: str = Field(..., description="脚本名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    script_type: str = Field(default="shell", description="脚本类型: shell/python")
    parameters: Optional[List[Dict[str, Any]]] = Field(default=None, description="参数定义JSON")
    timeout: int = Field(default=300, description="超时时间(秒)", ge=1, le=3600)


class ScriptCreate(ScriptBase):
    """创建脚本 Schema"""
    file_path: str = Field(..., description="脚本文件路径", min_length=1)


class ScriptUpdate(BaseModel):
    """更新脚本 Schema"""
    name: Optional[str] = Field(None, description="脚本名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    file_path: Optional[str] = Field(None, description="脚本文件路径", min_length=1)
    script_type: Optional[str] = Field(None, description="脚本类型: shell/python")
    parameters: Optional[List[Dict[str, Any]]] = Field(None, description="参数定义JSON")
    timeout: Optional[int] = Field(None, description="超时时间(秒)", ge=1, le=3600)


class ScriptResponse(ScriptBase):
    """脚本响应 Schema"""
    id: int
    file_path: Optional[str] = None
    source_file_name: Optional[str] = None
    content: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScriptListResponse(BaseModel):
    """脚本列表响应"""
    code: int = 200
    message: str = "success"
    data: List[ScriptResponse]
    total: int


class ScriptTestRequest(BaseModel):
    """脚本测试执行请求"""
    script_id: int = Field(..., description="脚本ID")
    server_id: int = Field(..., description="服务器ID")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="参数值")


class ScriptDistributeRequest(BaseModel):
    """脚本分发请求"""

    server_ids: List[int] = Field(..., description="目标服务器ID列表", min_length=1)
    target_directory: str = Field(..., description="目标目录")
    file_name: Optional[str] = Field(None, description="目标文件名（可选）")
