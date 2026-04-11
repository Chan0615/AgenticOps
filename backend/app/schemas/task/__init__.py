"""定时任务相关 Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class ScheduledTaskBase(BaseModel):
    """定时任务基础 Schema"""
    name: str = Field(..., description="任务名称", max_length=100)
    project_id: Optional[int] = Field(None, description="所属项目ID")
    group_id: Optional[int] = Field(None, description="所属分组ID")
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
    project_id: Optional[int] = Field(None, description="所属项目ID")
    group_id: Optional[int] = Field(None, description="所属分组ID")
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
    project_name: Optional[str] = None
    group_name: Optional[str] = None
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


class CronValidateRequest(BaseModel):
    cron_expression: str = Field(..., description="Cron表达式", min_length=1, max_length=100)


class CronNaturalConvertRequest(BaseModel):
    text: str = Field(..., description="自然语言表达式", min_length=1, max_length=100)


class CronPreviewRequest(BaseModel):
    cron_expression: str = Field(..., description="Cron表达式", min_length=1, max_length=100)
    count: int = Field(default=7, ge=1, le=20, description="预览次数")
    start_time: Optional[datetime] = Field(None, description="开始时间，默认当前时间")


class CronValidationData(BaseModel):
    valid: bool
    cron_expression: str
    description_zh: Optional[str] = None
    error: Optional[str] = None


class CronValidationResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: CronValidationData


class CronNaturalConvertData(BaseModel):
    text: str
    cron_expression: str
    description_zh: str


class CronNaturalConvertResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: CronNaturalConvertData


class CronPreviewData(BaseModel):
    cron_expression: str
    start_time: datetime
    next_runs: List[datetime]


class CronPreviewResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: CronPreviewData
