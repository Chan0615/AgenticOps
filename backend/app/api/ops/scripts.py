"""脚本管理 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.schemas.script import (
    ScriptCreate,
    ScriptUpdate,
    ScriptResponse,
    ScriptListResponse,
    ScriptTestRequest,
)
from app.crud.ops import script as script_crud
from app.api.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/scripts", tags=["脚本管理"])


@router.get("", response_model=ScriptListResponse)
async def list_scripts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="脚本名称"),
    script_type: Optional[str] = Query(None, description="脚本类型"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取脚本列表"""
    skip = (page - 1) * page_size
    scripts, total = await script_crud.get_scripts(
        db, skip=skip, limit=page_size, name=name, script_type=script_type
    )
    
    return ScriptListResponse(
        code=200,
        message="success",
        data=[ScriptResponse.model_validate(s) for s in scripts],
        total=total,
    )


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(
    script_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取脚本详情"""
    script = await script_crud.get_script(db, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")
    return script


@router.post("", response_model=ScriptResponse)
async def create_script(
    script: ScriptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建脚本"""
    db_script = await script_crud.create_script(
        db, script, created_by=current_user.get("username")
    )
    return db_script


@router.put("/{script_id}", response_model=ScriptResponse)
async def update_script(
    script_id: int,
    script: ScriptUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """更新脚本"""
    db_script = await script_crud.update_script(db, script_id, script)
    if not db_script:
        raise HTTPException(status_code=404, detail="脚本不存在")
    return db_script


@router.delete("/{script_id}")
async def delete_script(
    script_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """删除脚本"""
    success = await script_crud.delete_script(db, script_id)
    if not success:
        raise HTTPException(status_code=404, detail="脚本不存在")
    return {"code": 200, "message": "删除成功"}


@router.post("/test")
async def test_script(
    request: ScriptTestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """测试执行脚本"""
    # 获取脚本
    script = await script_crud.get_script(db, request.script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")
    
    # TODO: 实现脚本测试执行
    # 1. 获取服务器信息
    # 2. 替换脚本中的参数
    # 3. 执行脚本 (SSH 或 Salt)
    # 4. 返回执行结果
    
    return {
        "code": 200,
        "message": "脚本测试执行待实现",
        "data": {
            "script_id": request.script_id,
            "server_id": request.server_id,
            "parameters": request.parameters,
        },
    }
