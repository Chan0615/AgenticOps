"""定时任务调度器"""

import logging
from datetime import datetime
from celery_app import celery_app
from croniter import croniter
from app.tasks.salt_tasks import execute_salt_command
from app.tasks.ssh_tasks import execute_ssh_command

logger = logging.getLogger(__name__)


@celery_app.task(queue="scheduler")
def check_and_execute_tasks():
    """
    检查并执行到期的定时任务
    每分钟调用一次,扫描所有启用的任务
    """
    try:
        logger.info("开始检查定时任务...")
        
        # TODO: 从数据库查询所有启用的定时任务
        # SELECT * FROM ops_scheduled_task WHERE enabled = true
        
        # 临时方案: 返回占位日志
        # 后续实现数据库查询后,这里会:
        # 1. 查询所有 enabled=True 的任务
        # 2. 检查每个任务的 cron_expression
        # 3. 如果当前时间匹配,则触发执行
        # 4. 更新 last_run_at 和 next_run_at
        
        logger.info("定时任务检查完成 (待实现数据库查询)")
        
        return {
            "status": "success",
            "message": "检查完成,待实现数据库查询逻辑",
            "checked_at": datetime.now().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"检查定时任务失败: {e}")
        return {
            "status": "failed",
            "error": str(e),
        }


def should_execute_task(cron_expression: str, last_run_at: datetime = None) -> bool:
    """
    判断任务是否应该执行
    
    Args:
        cron_expression: Cron表达式
        last_run_at: 上次执行时间
        
    Returns:
        bool: 是否应该执行
    """
    try:
        now = datetime.now()
        cron = croniter(cron_expression, now)
        
        # 获取下次执行时间
        next_run = cron.get_next(datetime)
        
        # 如果 last_run_at 为空或早于下次执行时间,则应该执行
        if last_run_at is None or last_run_at < next_run:
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"解析 Cron 表达式失败: {cron_expression}, error: {e}")
        return False
