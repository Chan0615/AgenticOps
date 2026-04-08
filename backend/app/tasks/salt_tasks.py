"""SaltStack 异步任务"""

import logging
from datetime import datetime
from celery_app import celery_app
from app.services.salt_service import salt_service
from app.db.database import AsyncSessionLocal
from app.models.ops import TaskExecutionLog
from sqlalchemy import select

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, queue="salt")
def execute_salt_command(self, task_id: int, server_ids: list, command: str, salt_env: str = "fuchunyun"):
    """
    通过 SaltStack 执行命令
    
    Args:
        task_id: 定时任务ID
        server_ids: 服务器ID列表
        command: 执行的命令
        salt_env: Salt环境名称
    """
    try:
        logger.info(f"开始执行 Salt 任务: task_id={task_id}, servers={server_ids}")
        
        # 获取 Salt Minion IDs (这里简化处理,实际应该从数据库查询)
        # target = "L@minion1,minion2,minion3"  # 列表匹配
        target = "*"  # 临时使用全部,后续优化
        
        # 执行命令
        result = salt_service.run_shell_command(salt_env, target, command)
        
        logger.info(f"Salt 任务执行完成: {result}")
        
        # 保存执行日志 (同步方式,因为 Celery 任务中不宜使用异步数据库)
        # 这里需要改为同步数据库操作或调用API
        return {
            "status": "success",
            "result": result,
            "task_id": task_id,
        }
        
    except Exception as e:
        logger.error(f"Salt 任务执行失败: {e}")
        
        # 重试
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60)  # 1分钟后重试
        
        return {
            "status": "failed",
            "error": str(e),
            "task_id": task_id,
        }


@celery_app.task(bind=True, max_retries=3, queue="salt")
def test_salt_connection(self, salt_env: str = "fuchunyun", target: str = "*"):
    """
    测试 Salt 连接
    
    Args:
        salt_env: Salt环境名称
        target: 目标Minion
    """
    try:
        logger.info(f"测试 Salt 连接: env={salt_env}, target={target}")
        result = salt_service.test_ping(salt_env, target)
        logger.info(f"Salt 连接测试结果: {result}")
        return result
    except Exception as e:
        logger.error(f"Salt 连接测试失败: {e}")
        raise
