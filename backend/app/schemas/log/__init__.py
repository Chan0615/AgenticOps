"""操作日志相关 Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskExecutionLogBase(BaseModel):
    """任务执行日志基础 Schema"""
    task_id: Optional[int] = Field(None, description="任务ID")
    server_id: Optional[int] = Field(None, description="服务器ID")
    status: str = Field(default="pending", description="状态: pending/running/success/failed")
    command: str = Field(..., description="执行的命令")


class TaskExecutionLogResponse(TaskExecutionLogBase):
    """任务执行日志响应 Schema"""
    id: int
    task_name: Optional[str] = None
    server_ip: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    exit_code: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TaskExecutionLogListResponse(BaseModel):
    """任务执行日志列表响应"""
    code: int = 200
    message: str = "success"
    data: List[TaskExecutionLogResponse]
    total: int


class OperationLogQuery(BaseModel):
    """操作日志查询参数"""
    module: Optional[str] = Field(None, description="模块: server/script/task")
    action: Optional[str] = Field(None, description="操作: create/update/delete/execute")
    user_id: Optional[int] = Field(None, description="用户ID")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    page: int = Field(default=1, description="页码", ge=1)
    page_size: int = Field(default=20, description="每页数量", ge=1, le=100)
