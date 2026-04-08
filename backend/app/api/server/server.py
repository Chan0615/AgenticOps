"""服务器管理 API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.services.salt_service import salt_service
from app.services.ssh_service import ssh_manager

router = APIRouter(prefix="/server", tags=["服务器管理"])


# ============ SaltStack 管理 ============

@router.post("/salt/{env_name}/execute")
async def salt_execute(
    env_name: str,
    target: str,
    fun: str,
    arg: Optional[list] = None,
    db: AsyncSession = Depends(get_db),
):
    """执行 Salt 命令"""
    try:
        result = await salt_service.run_command(env_name, target, fun, arg)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/salt/{env_name}/minions")
async def salt_get_minions(env_name: str, db: AsyncSession = Depends(get_db)):
    """获取 Minion 列表"""
    try:
        result = await salt_service.get_minions(env_name)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/salt/{env_name}/ping")
async def salt_ping(env_name: str, target: str = "*", db: AsyncSession = Depends(get_db)):
    """测试 Minion 连接"""
    try:
        result = await salt_service.test_ping(env_name, target)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/salt/{env_name}/command")
async def salt_run_command(
    env_name: str,
    target: str,
    command: str,
    db: AsyncSession = Depends(get_db),
):
    """执行 Shell 命令"""
    try:
        result = await salt_service.run_shell_command(env_name, target, command)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ SSH 管理 ============

@router.post("/ssh/execute")
async def ssh_execute(
    server_id: str,
    hostname: str,
    command: str,
    port: int = 22,
    username: str = "root",
    password: Optional[str] = None,
    private_key: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """SSH 执行命令"""
    try:
        conn = ssh_manager.get_connection(
            server_id, hostname, port, username, password, private_key
        )
        result = conn.execute_command(command)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ssh/disconnect/{server_id}")
async def ssh_disconnect(server_id: str, db: AsyncSession = Depends(get_db)):
    """断开 SSH 连接"""
    try:
        ssh_manager.remove_connection(server_id)
        return {"success": True, "message": "连接已断开"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
