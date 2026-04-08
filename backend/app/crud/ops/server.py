"""服务器 CRUD 操作"""

from typing import List, Optional
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ops import Server
from app.schemas.server.server import ServerCreate, ServerUpdate
import logging

logger = logging.getLogger(__name__)


async def get_server(db: AsyncSession, server_id: int) -> Optional[Server]:
    """根据ID获取服务器"""
    result = await db.execute(select(Server).where(Server.id == server_id))
    return result.scalar_one_or_none()


async def get_servers(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = None,
    environment: Optional[str] = None,
    status: Optional[str] = None,
) -> tuple[List[Server], int]:
    """获取服务器列表"""
    query = select(Server)
    count_query = select(func.count(Server.id))
    
    # 添加过滤条件
    if name:
        query = query.where(Server.name.ilike(f"%{name}%"))
        count_query = count_query.where(Server.name.ilike(f"%{name}%"))
    
    if environment:
        query = query.where(Server.environment == environment)
        count_query = count_query.where(Server.environment == environment)
    
    if status:
        query = query.where(Server.status == status)
        count_query = count_query.where(Server.status == status)
    
    # 获取总数
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    query = query.offset(skip).limit(limit).order_by(Server.created_at.desc())
    result = await db.execute(query)
    servers = result.scalars().all()
    
    return servers, total


async def create_server(db: AsyncSession, server: ServerCreate, created_by: str = None) -> Server:
    """创建服务器"""
    db_server = Server(
        **server.model_dump(),
        created_by=created_by,
    )
    db.add(db_server)
    await db.commit()
    await db.refresh(db_server)
    return db_server


async def update_server(db: AsyncSession, server_id: int, server: ServerUpdate) -> Optional[Server]:
    """更新服务器"""
    db_server = await get_server(db, server_id)
    if not db_server:
        return None
    
    update_data = server.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_server, field, value)
    
    await db.commit()
    await db.refresh(db_server)
    return db_server


async def delete_server(db: AsyncSession, server_id: int) -> bool:
    """删除服务器"""
    db_server = await get_server(db, server_id)
    if not db_server:
        return False
    
    await db.delete(db_server)
    await db.commit()
    return True


async def update_server_status(db: AsyncSession, server_id: int, status: str) -> Optional[Server]:
    """更新服务器状态"""
    db_server = await get_server(db, server_id)
    if not db_server:
        return None
    
    db_server.status = status
    await db.commit()
    await db.refresh(db_server)
    return db_server


async def test_server_connection(server: Server) -> dict:
    """测试服务器连接"""
    from app.services.ssh_service import SSHConnection
    
    try:
        ssh_conn = SSHConnection(
            hostname=server.hostname,
            port=server.port,
            username=server.username,
            password=server.password if server.auth_type == "password" else None,
            private_key=server.private_key if server.auth_type == "key" else None,
        )
        
        ssh_conn.connect()
        
        # 执行简单命令测试
        result = ssh_conn.execute_command("echo 'Connection test successful'")
        ssh_conn.close()
        
        return {
            "success": True,
            "message": "连接成功",
            "response_time": None,  # TODO: 计算响应时间
        }
        
    except Exception as e:
        logger.error(f"服务器连接测试失败: {e}")
        return {
            "success": False,
            "message": f"连接失败: {str(e)}",
        }
