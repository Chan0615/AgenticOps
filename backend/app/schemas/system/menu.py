from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ 菜单相关 ============
class MenuBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=50)
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0
    type: str = "menu"
    meta: Optional[dict] = None
    description: Optional[str] = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    type: Optional[str] = None
    status: Optional[bool] = None
    meta: Optional[dict] = None
    description: Optional[str] = None


class MenuResponse(MenuBase):
    id: int
    status: bool
    created_at: datetime
    updated_at: datetime
    children: List["MenuResponse"] = []
    
    class Config:
        from_attributes = True


# 更新前向引用
MenuResponse.model_rebuild()
