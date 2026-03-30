from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any
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


class MenuResponse(BaseModel):
    id: int
    name: str
    code: str
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0
    type: str = "menu"
    status: bool = True
    meta: Optional[dict] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    children: List["MenuResponse"] = []

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def extract_data(cls, obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
            if "children" not in data or data["children"] is None:
                data["children"] = []
            return data
        return obj


# 更新前向引用
MenuResponse.model_rebuild()
