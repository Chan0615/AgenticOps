"""
运维 AI 助手 Schemas

定义运维 AI 对话接口的请求/响应数据结构。
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


# ============ 请求 ============

class OpsChatRequest(BaseModel):
    """运维 AI 对话请求"""
    message: str = Field(..., min_length=1, description="用户消息")
    conversation_id: Optional[int] = Field(None, description="对话 ID，不填则创建新对话")


class OpsConfirmRequest(BaseModel):
    """用户确认写操作请求"""
    tool_name: str = Field(..., description="要执行的工具名称")
    tool_args: dict = Field(..., description="工具参数")
    conversation_id: int = Field(..., description="所属对话 ID")


# ============ 响应 ============

class PendingAction(BaseModel):
    """
    待确认的写操作

    当 AI 决定调用写操作工具时，后端不直接执行，
    而是将操作信息封装成此结构返回给前端，
    由前端弹出确认框，用户确认后再调用 /confirm 接口真正执行。
    """
    tool_name: str = Field(..., description="工具函数名")
    tool_args: dict = Field(..., description="工具参数")
    description: str = Field(..., description="AI 生成的操作描述（用于前端确认框展示）")


class OpsChatResponse(BaseModel):
    """运维 AI 对话响应"""
    conversation_id: int = Field(..., description="对话 ID")
    answer: str = Field(..., description="AI 回复文本")
    pending_action: Optional[PendingAction] = Field(
        None, description="待确认的写操作（非空时前端显示确认框）"
    )
    sources: List[str] = Field(default_factory=list, description="数据来源标注")


class OpsConfirmResponse(BaseModel):
    """写操作确认执行响应"""
    conversation_id: int = Field(..., description="对话 ID")
    answer: str = Field(..., description="执行结果描述")
    success: bool = Field(..., description="是否执行成功")


# ============ 对话历史（复用 agent schema）============

class OpsConversationItem(BaseModel):
    """对话列表项"""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
