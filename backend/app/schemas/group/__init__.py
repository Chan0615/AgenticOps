"""项目与分组 Schema"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OpsProjectBase(BaseModel):
    """运维项目基础 Schema"""

    name: str = Field(..., description="项目名称", max_length=100)
    code: str = Field(..., description="项目编码", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)


class OpsProjectCreate(OpsProjectBase):
    """创建运维项目 Schema"""


class OpsProjectUpdate(BaseModel):
    """更新运维项目 Schema"""

    name: Optional[str] = Field(None, description="项目名称", max_length=100)
    code: Optional[str] = Field(None, description="项目编码", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)


class OpsProjectResponse(OpsProjectBase):
    """运维项目响应 Schema"""

    id: int
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OpsProjectListResponse(BaseModel):
    """运维项目列表响应"""

    code: int = 200
    message: str = "success"
    data: List[OpsProjectResponse]
    total: int


class OpsGroupBase(BaseModel):
    """运维分组基础 Schema"""

    project_id: int = Field(..., description="所属项目ID")
    name: str = Field(..., description="分组名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)


class OpsGroupCreate(OpsGroupBase):
    """创建运维分组 Schema"""


class OpsGroupUpdate(BaseModel):
    """更新运维分组 Schema"""

    project_id: Optional[int] = Field(None, description="所属项目ID")
    name: Optional[str] = Field(None, description="分组名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)


class OpsGroupResponse(OpsGroupBase):
    """运维分组响应 Schema"""

    id: int
    project_name: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OpsGroupListResponse(BaseModel):
    """运维分组列表响应"""

    code: int = 200
    message: str = "success"
    data: List[OpsGroupResponse]
    total: int
