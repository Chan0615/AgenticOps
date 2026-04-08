"""SSH 异步任务"""

import logging
from datetime import datetime
from celery_app import celery_app
from app.services.ssh_service import SSHConnection
from app.models.ops import TaskExecutionLog, Server
from app.db.database import AsyncSessionLocal
from sqlalchemy import select

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, queue="ssh")
def execute_ssh_command(self, task_id: int, server_id: int, command: str, timeout: int = 300):
    """
    通过 SSH 执行命令
    
    Args:
        task_id: 定时任务ID
        server_id: 服务器ID
        command: 执行的命令
        timeout: 超时时间(秒)
    """
    started_at = datetime.now()
    ssh_conn = None
    
    try:
        logger.info(f"开始执行 SSH 任务: task_id={task_id}, server_id={server_id}")
        
        # 注意: Celery 任务中需要使用同步数据库查询
        # 这里简化处理,实际应该通过 API 或同步方式获取服务器信息
        # 后续需要实现同步数据库查询或使用 HTTP API
        
        # 临时方案: 返回占位结果
        # TODO: 实现同步数据库查询获取服务器配置
        return {
            "status": "pending",
            "message": "SSH任务待实现同步数据库查询",
            "task_id": task_id,
            "server_id": server_id,
        }
        
        # 以下代码待实现同步数据库后启用
        """
        # 获取服务器配置
        server = await get_server_by_id(server_id)
        
        # 创建 SSH 连接
        ssh_conn = SSHConnection(
            hostname=server.hostname,
            port=server.port,
            username=server.username,
            password=server.password,
            private_key=server.private_key,
        )
        ssh_conn.connect()
        
        # 执行命令
        result = ssh_conn.execute_command(command)
        
        finished_at = datetime.now()
        duration = (finished_at - started_at).total_seconds()
        
        # 保存执行日志
        await save_execution_log(
            task_id=task_id,
            server_id=server_id,
            status="success" if result["exit_code"] == 0 else "failed",
            command=command,
            output=result["output"],
            error=result["error"],
            exit_code=result["exit_code"],
            started_at=started_at,
            finished_at=finished_at,
            duration=duration,
        )
        
        return {
            "status": "success",
            "result": result,
            "task_id": task_id,
            "server_id": server_id,
        }
        """
        
    except Exception as e:
        logger.error(f"SSH 任务执行失败: {e}")
        
        finished_at = datetime.now()
        duration = (finished_at - started_at).total_seconds()
        
        # 重试
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60)
        
        return {
            "status": "failed",
            "error": str(e),
            "task_id": task_id,
            "server_id": server_id,
        }
    finally:
        if ssh_conn:
            ssh_conn.close()


@celery_app.task(bind=True, max_retries=3, queue="ssh")
def test_ssh_connection(self, server_id: int):
    """
    测试 SSH 连接
    
    Args:
        server_id: 服务器ID
    """
    try:
        logger.info(f"测试 SSH 连接: server_id={server_id}")
        
        # TODO: 实现同步数据库查询
        return {
            "status": "pending",
            "message": "SSH连接测试待实现同步数据库查询",
        }
        
    except Exception as e:
        logger.error(f"SSH 连接测试失败: {e}")
        raise
