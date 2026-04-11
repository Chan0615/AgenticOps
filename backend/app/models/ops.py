"""
服务器、脚本、任务相关模型
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Server(Base):
    """服务器模型"""

    __tablename__ = "ops_server"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="服务器名称")
    hostname = Column(String(255), nullable=False, comment="IP地址或域名")
    port = Column(Integer, default=22, comment="SSH端口")
    username = Column(String(50), default="root", comment="登录用户名")
    salt_minion_id = Column(String(100), nullable=True, comment="Salt Minion ID")
    environment = Column(String(50), default="production", comment="环境: production/staging/testing")
    tags = Column(JSON, nullable=True, comment="标签列表")
    status = Column(String(20), default="offline", comment="状态: online/offline/unknown")
    description = Column(String(500), nullable=True, comment="描述")
    created_by = Column(String(50), nullable=True, comment="创建人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    execution_logs = relationship("TaskExecutionLog", back_populates="server")


class OpsProject(Base):
    """运维项目模型"""

    __tablename__ = "ops_project"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="项目名称")
    code = Column(String(100), nullable=False, unique=True, comment="项目编码")
    description = Column(String(500), nullable=True, comment="描述")
    created_by = Column(String(50), nullable=True, comment="创建人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    groups = relationship("OpsGroup", back_populates="project", cascade="all, delete-orphan")
    scripts = relationship("Script", back_populates="project")
    tasks = relationship("ScheduledTask", back_populates="project")


class OpsGroup(Base):
    """运维分组模型"""

    __tablename__ = "ops_group"
    __table_args__ = (
        UniqueConstraint("project_id", "name", name="uq_ops_group_project_name"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(
        Integer,
        ForeignKey("ops_project.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属项目ID",
    )
    name = Column(String(100), nullable=False, comment="分组名称")
    description = Column(String(500), nullable=True, comment="描述")
    created_by = Column(String(50), nullable=True, comment="创建人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    project = relationship("OpsProject", back_populates="groups")
    scripts = relationship("Script", back_populates="group")
    tasks = relationship("ScheduledTask", back_populates="group")


class Script(Base):
    """脚本模型"""

    __tablename__ = "ops_script"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="脚本名称")
    project_id = Column(
        Integer, ForeignKey("ops_project.id", ondelete="SET NULL"), nullable=True, index=True, comment="所属项目ID"
    )
    group_id = Column(
        Integer, ForeignKey("ops_group.id", ondelete="SET NULL"), nullable=True, index=True, comment="所属分组ID"
    )
    description = Column(String(500), nullable=True, comment="描述")
    content = Column(Text, nullable=False, comment="脚本内容")
    script_type = Column(String(20), default="shell", comment="脚本类型: shell/python")
    parameters = Column(JSON, nullable=True, comment="参数定义JSON")
    timeout = Column(Integer, default=300, comment="超时时间(秒)")
    created_by = Column(String(50), nullable=True, comment="创建人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    project = relationship("OpsProject", back_populates="scripts")
    group = relationship("OpsGroup", back_populates="scripts")
    tasks = relationship("ScheduledTask", back_populates="script")
    versions = relationship("OpsScriptVersion", back_populates="script", cascade="all, delete-orphan")


class OpsScriptVersion(Base):
    """脚本版本模型"""

    __tablename__ = "ops_script_version"
    __table_args__ = (
        UniqueConstraint("script_id", "version_no", name="uq_ops_script_version_script_no"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    script_id = Column(
        Integer,
        ForeignKey("ops_script.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="脚本ID",
    )
    version_no = Column(Integer, nullable=False, comment="版本号")
    file_path = Column(String(500), nullable=False, comment="脚本文件路径")
    source_file_name = Column(String(255), nullable=True, comment="源文件名")
    note = Column(String(500), nullable=True, comment="版本备注")
    created_by = Column(String(50), nullable=True, comment="上传人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    script = relationship("Script", back_populates="versions")


class ScheduledTask(Base):
    """定时任务模型"""

    __tablename__ = "ops_scheduled_task"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="任务名称")
    project_id = Column(
        Integer, ForeignKey("ops_project.id", ondelete="SET NULL"), nullable=True, index=True, comment="所属项目ID"
    )
    group_id = Column(
        Integer, ForeignKey("ops_group.id", ondelete="SET NULL"), nullable=True, index=True, comment="所属分组ID"
    )
    description = Column(String(500), nullable=True, comment="描述")
    script_id = Column(
        Integer, ForeignKey("ops_script.id", ondelete="SET NULL"), nullable=True, comment="关联脚本ID"
    )
    server_ids = Column(JSON, nullable=False, comment="目标服务器ID列表")
    cron_expression = Column(String(100), nullable=False, comment="Cron表达式")
    task_type = Column(String(20), default="salt", comment="执行方式: salt")
    command = Column(Text, nullable=True, comment="自定义命令(不使用脚本时)")
    enabled = Column(Boolean, default=True, comment="是否启用")
    celery_task_id = Column(String(255), nullable=True, comment="Celery定时任务ID")
    last_run_at = Column(DateTime, nullable=True, comment="上次执行时间")
    next_run_at = Column(DateTime, nullable=True, comment="下次执行时间")
    created_by = Column(String(50), nullable=True, comment="创建人")
    updated_by = Column(String(50), nullable=True, comment="修改人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    project = relationship("OpsProject", back_populates="tasks")
    group = relationship("OpsGroup", back_populates="tasks")
    script = relationship("Script", back_populates="tasks")
    execution_logs = relationship("TaskExecutionLog", back_populates="task")


class TaskExecutionLog(Base):
    """任务执行日志模型"""

    __tablename__ = "ops_task_execution_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(
        Integer, ForeignKey("ops_scheduled_task.id", ondelete="CASCADE"), nullable=True, comment="任务ID"
    )
    server_id = Column(
        Integer, ForeignKey("ops_server.id", ondelete="SET NULL"), nullable=True, comment="服务器ID"
    )
    status = Column(String(20), default="pending", comment="状态: pending/running/success/failed")
    command = Column(Text, nullable=False, comment="执行的命令")
    output = Column(Text, nullable=True, comment="标准输出")
    error = Column(Text, nullable=True, comment="错误输出")
    exit_code = Column(Integer, nullable=True, comment="退出码")
    started_at = Column(DateTime, nullable=True, comment="开始时间")
    finished_at = Column(DateTime, nullable=True, comment="结束时间")
    duration = Column(Float, nullable=True, comment="执行时长(秒)")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关联关系
    task = relationship("ScheduledTask", back_populates="execution_logs")
    server = relationship("Server", back_populates="execution_logs")
