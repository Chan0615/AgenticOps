"""服务器管理 API"""

import time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.services.salt_service import salt_service
from app.services.ssh_service import ssh_manager
from app.crud.server import server as server_crud
from app.schemas.server.server import (
    ServerCreate,
    ServerUpdate,
    ServerResponse,
    ServerListResponse,
    ServerGroupCreate,
    ServerGroupResponse,
    ConnectivityCheckResponse,
)
from app.core.log_decorator import log_operation

router = APIRouter(prefix="/server", tags=["服务器管理"])


# ============ 服务器分组管理 ============

@router.post("/groups", response_model=ServerGroupResponse)
@log_operation(module="服务器管理", action="创建分组", description="创建服务器分组")
async def create_server_group(
    group_data: ServerGroupCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建服务器分组"""
    group = await server_crud.create_server_group(
        db=db,
        name=group_data.name,
        environment=group_data.environment,
        description=group_data.description,
    )
    return group


@router.get("/groups", response_model=list[ServerGroupResponse])
async def get_server_groups(db: AsyncSession = Depends(get_db)):
    """获取所有服务器分组"""
    groups = await server_crud.get_server_groups(db)
    return groups


# ============ 服务器 CRUD ============

@router.post("/", response_model=ServerResponse)
@log_operation(module="服务器管理", action="创建服务器", description="添加新服务器")
async def create_server(
    server_data: ServerCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建服务器"""
    server = await server_crud.create_server(
        db=db,
        name=server_data.name,
        hostname=server_data.hostname,
        port=server_data.port,
        username=server_data.username,
        password=server_data.password,
        private_key=server_data.private_key,
        os_type=server_data.os_type,
        group_id=server_data.group_id,
        salt_minion_id=server_data.salt_minion_id,
        tags=server_data.tags,
    )
    return server


@router.get("/", response_model=ServerListResponse)
async def get_servers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="搜索关键词"),
    environment: Optional[str] = Query(None, description="环境过滤"),
    status: Optional[bool] = Query(None, description="状态过滤"),
    db: AsyncSession = Depends(get_db),
):
    """获取服务器列表（支持搜索和过滤）"""
    servers = await server_crud.get_servers(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        environment=environment,
        status=status,
    )
    
    # 获取总数
    total_servers = await server_crud.get_servers(
        db=db,
        skip=0,
        limit=10000,
        search=search,
        environment=environment,
        status=status,
    )
    
    return ServerListResponse(
        total=len(total_servers),
        items=servers,
    )


@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(server_id: int, db: AsyncSession = Depends(get_db)):
    """获取服务器详情"""
    server = await server_crud.get_server_by_id(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    return server


@router.put("/{server_id}", response_model=ServerResponse)
@log_operation(module="服务器管理", action="更新服务器", description="更新服务器信息")
async def update_server(
    server_id: int,
    server_data: ServerUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新服务器"""
    update_data = server_data.dict(exclude_unset=True)
    server = await server_crud.update_server(db, server_id, **update_data)
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    return server


@router.delete("/{server_id}")
@log_operation(module="服务器管理", action="删除服务器", description="删除服务器")
async def delete_server(server_id: int, db: AsyncSession = Depends(get_db)):
    """删除服务器"""
    success = await server_crud.delete_server(db, server_id)
    if not success:
        raise HTTPException(status_code=404, detail="服务器不存在")
    return {"message": "服务器已删除"}


# ============ 连通性检测 ============

@router.post("/{server_id}/check-connectivity", response_model=ConnectivityCheckResponse)
@log_operation(module="服务器管理", action="检测连通性", description="检测服务器连通性")
async def check_server_connectivity(
    server_id: int,
    db: AsyncSession = Depends(get_db),
):
    """检测服务器连通性（SSH Ping）"""
    server = await server_crud.get_server_by_id(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    
    start_time = time.time()
    is_connected = False
    error_message = None
    
    try:
        # 尝试 SSH 连接
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if server.private_key:
            from io import StringIO
            key = paramiko.RSAKey.from_private_key(StringIO(server.private_key))
            client.connect(
                hostname=server.hostname,
                port=server.port,
                username=server.username,
                pkey=key,
                timeout=5,
            )
        else:
            client.connect(
                hostname=server.hostname,
                port=server.port,
                username=server.username,
                password=server.password,
                timeout=5,
            )
        
        # 执行简单命令测试
        stdin, stdout, stderr = client.exec_command("echo ping", timeout=5)
        output = stdout.read().decode().strip()
        
        if output == "ping":
            is_connected = True
        
        client.close()
        
    except Exception as e:
        error_message = str(e)
        is_connected = False
    
    response_time = (time.time() - start_time) * 1000  # 毫秒
    
    # 更新数据库中的连通性状态
    await server_crud.update_server_connectivity(db, server_id, is_connected)
    
    return ConnectivityCheckResponse(
        server_id=server_id,
        hostname=server.hostname,
        is_connected=is_connected,
        response_time=round(response_time, 2),
        error_message=error_message,
    )


@router.post("/check-all-connectivity")
@log_operation(module="服务器管理", action="批量检测连通性", description="批量检测所有服务器连通性")
async def check_all_servers_connectivity(db: AsyncSession = Depends(get_db)):
    """批量检测所有服务器连通性"""
    servers = await server_crud.get_servers(db, skip=0, limit=10000)
    
    results = []
    for server in servers:
        start_time = time.time()
        is_connected = False
        error_message = None
        
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if server.private_key:
                from io import StringIO
                key = paramiko.RSAKey.from_private_key(StringIO(server.private_key))
                client.connect(
                    hostname=server.hostname,
                    port=server.port,
                    username=server.username,
                    pkey=key,
                    timeout=5,
                )
            else:
                client.connect(
                    hostname=server.hostname,
                    port=server.port,
                    username=server.username,
                    password=server.password,
                    timeout=5,
                )
            
            stdin, stdout, stderr = client.exec_command("echo ping", timeout=5)
            output = stdout.read().decode().strip()
            
            if output == "ping":
                is_connected = True
            
            client.close()
            
        except Exception as e:
            error_message = str(e)
            is_connected = False
        
        response_time = (time.time() - start_time) * 1000
        
        # 更新数据库
        await server_crud.update_server_connectivity(db, server.id, is_connected)
        
        results.append({
            "server_id": server.id,
            "hostname": server.hostname,
            "is_connected": is_connected,
            "response_time": round(response_time, 2),
            "error_message": error_message,
        })
    
    return {"total": len(results), "results": results}
