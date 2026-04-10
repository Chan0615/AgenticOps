"""定时任务相关 Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class ScheduledTaskBase(BaseModel):
    """定时任务基础 Schema"""
    name: str = Field(..., description="任务名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    script_id: Optional[int] = Field(None, description="关联脚本ID")
    server_ids: List[int] = Field(..., description="目标服务器ID列表", min_length=1)
    cron_expression: str = Field(..., description="Cron表达式", max_length=100)
    task_type: Literal["salt"] = Field(default="salt", description="执行方式: salt")
    command: Optional[str] = Field(None, description="自定义命令(不使用脚本时)")
    enabled: bool = Field(default=True, description="是否启用")


class ScheduledTaskCreate(ScheduledTaskBase):
    """创建定时任务 Schema"""
    pass


class ScheduledTaskUpdate(BaseModel):
    """更新定时任务 Schema"""
    name: Optional[str] = Field(None, description="任务名称", max_length=100)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    script_id: Optional[int] = Field(None, description="关联脚本ID")
    server_ids: Optional[List[int]] = Field(None, description="目标服务器ID列表")
    cron_expression: Optional[str] = Field(None, description="Cron表达式", max_length=100)
    task_type: Optional[Literal["salt"]] = Field(None, description="执行方式: salt")
    command: Optional[str] = Field(None, description="自定义命令(不使用脚本时)")
    enabled: Optional[bool] = Field(None, description="是否启用")


class ScheduledTaskResponse(ScheduledTaskBase):
    """定时任务响应 Schema"""
    id: int
    celery_task_id: Optional[str] = None
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScheduledTaskListResponse(BaseModel):
    """定时任务列表响应"""
    code: int = 200
    message: str = "success"
    data: List[ScheduledTaskResponse]
    total: int


class TaskManualTriggerRequest(BaseModel):
    """手动触发任务请求"""
    task_id: int = Field(..., description="任务ID")
