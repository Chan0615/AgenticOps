from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ 角色相关 ============
class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    code: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    sort_order: int = 0


class RoleCreate(RoleBase):
    menu_ids: Optional[List[int]] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[bool] = None
    menu_ids: Optional[List[int]] = None


class RoleResponse(RoleBase):
    id: int
    status: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
