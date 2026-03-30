from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any
from datetime import datetime


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


class RoleResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    sort_order: int = 0
    status: bool
    menu_ids: List[int] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def extract_menu_ids(cls, obj: Any) -> Any:
        if hasattr(obj, "permissions") and hasattr(obj, "__dict__"):
            data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
            data["menu_ids"] = (
                [p.menu_id for p in obj.permissions] if obj.permissions else []
            )
            return data
        return obj
