"""服务器 CRUD 操作"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_
from typing import Optional
from app.models.server import Server, ServerGroup


async def create_server(
    db: AsyncSession,
    name: str,
    hostname: str,
    username: str,
    port: int = 22,
    password: Optional[str] = None,
    private_key: Optional[str] = None,
    os_type: str = "linux",
    group_id: Optional[int] = None,
    salt_minion_id: Optional[str] = None,
    tags: Optional[dict] = None,
) -> Server:
    """创建服务器"""
    server = Server(
        name=name,
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        private_key=private_key,
        os_type=os_type,
        group_id=group_id,
        salt_minion_id=salt_minion_id,
        tags=tags,
    )
    db.add(server)
    await db.commit()
    await db.refresh(server)
    return server


async def get_server_by_id(db: AsyncSession, server_id: int) -> Optional[Server]:
    """根据ID获取服务器"""
    result = await db.execute(
        select(Server).where(Server.id == server_id)
    )
    return result.scalar_one_or_none()


async def get_servers(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    environment: Optional[str] = None,
    status: Optional[bool] = None,
) -> list[Server]:
    """获取服务器列表（支持搜索和过滤）"""
    query = select(Server)
    
    # 搜索条件
    if search:
        query = query.where(
            or_(
                Server.name.contains(search),
                Server.hostname.contains(search),
                Server.username.contains(search),
                Server.salt_minion_id.contains(search),
            )
        )
    
    # 环境过滤
    if environment:
        query = query.join(ServerGroup).where(ServerGroup.environment == environment)
    
    # 状态过滤
    if status is not None:
        query = query.where(Server.status == status)
    
    query = query.order_by(desc(Server.created_at))
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


async def update_server(
    db: AsyncSession,
    server_id: int,
    **kwargs,
) -> Optional[Server]:
    """更新服务器信息"""
    server = await get_server_by_id(db, server_id)
    if not server:
        return None
    
    for key, value in kwargs.items():
        if hasattr(server, key):
            setattr(server, key, value)
    
    await db.commit()
    await db.refresh(server)
    return server


async def delete_server(db: AsyncSession, server_id: int) -> bool:
    """删除服务器"""
    server = await get_server_by_id(db, server_id)
    if not server:
        return False
    
    await db.delete(server)
    await db.commit()
    return True


async def update_server_connectivity(
    db: AsyncSession,
    server_id: int,
    is_connected: bool,
) -> Optional[Server]:
    """更新服务器连通性状态"""
    from sqlalchemy.sql import func
    
    server = await get_server_by_id(db, server_id)
    if not server:
        return None
    
    server.status = is_connected
    if is_connected:
        server.last_connected_at = func.now()
    
    await db.commit()
    await db.refresh(server)
    return server


# ============ 服务器分组 CRUD ============

async def create_server_group(
    db: AsyncSession,
    name: str,
    environment: str,
    description: Optional[str] = None,
) -> ServerGroup:
    """创建服务器分组"""
    group = ServerGroup(
        name=name,
        environment=environment,
        description=description,
    )
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


async def get_server_groups(db: AsyncSession) -> list[ServerGroup]:
    """获取所有服务器分组"""
    result = await db.execute(select(ServerGroup).order_by(desc(ServerGroup.created_at)))
    return result.scalars().all()
