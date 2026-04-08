"""服务器管理 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.schemas.server.server import (
    ServerCreate,
    ServerUpdate,
    ServerResponse,
    ServerListResponse,
    ConnectionTestRequest,
)
from app.crud.ops import server as server_crud
from app.api.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/servers", tags=["服务器管理"])


@router.get("", response_model=ServerListResponse)
async def list_servers(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="服务器名称"),
    environment: Optional[str] = Query(None, description="环境"),
    status: Optional[str] = Query(None, description="状态"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取服务器列表"""
    skip = (page - 1) * page_size
    servers, total = await server_crud.get_servers(
        db, skip=skip, limit=page_size, name=name, environment=environment, status=status
    )
    
    return ServerListResponse(
        code=200,
        message="success",
        data=[ServerResponse.model_validate(s) for s in servers],
        total=total,
    )


@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(
    server_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取服务器详情"""
    server = await server_crud.get_server(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    return server


@router.post("", response_model=ServerResponse)
async def create_server(
    server: ServerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建服务器"""
    db_server = await server_crud.create_server(
        db, server, created_by=current_user.get("username")
    )
    return db_server


@router.put("/{server_id}", response_model=ServerResponse)
async def update_server(
    server_id: int,
    server: ServerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """更新服务器"""
    db_server = await server_crud.update_server(db, server_id, server)
    if not db_server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    return db_server


@router.delete("/{server_id}")
async def delete_server(
    server_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """删除服务器"""
    success = await server_crud.delete_server(db, server_id)
    if not success:
        raise HTTPException(status_code=404, detail="服务器不存在")
    return {"code": 200, "message": "删除成功"}


@router.post("/test-connection")
async def test_connection(
    request: ConnectionTestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """测试服务器连接"""
    server = await server_crud.get_server(db, request.server_id)
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    
    if request.test_type == "ssh":
        result = await server_crud.test_server_connection(server)
        
        # 更新服务器状态
        new_status = "online" if result["success"] else "offline"
        await server_crud.update_server_status(db, request.server_id, new_status)
        
        return {
            "code": 200 if result["success"] else 500,
            "message": result["message"],
            "data": result,
        }
    elif request.test_type == "salt":
        # TODO: 实现 Salt 连接测试
        return {
            "code": 200,
            "message": "Salt连接测试待实现",
        }
    else:
        raise HTTPException(status_code=400, detail="不支持的测试类型")
