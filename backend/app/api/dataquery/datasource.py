"""数据源管理 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.schemas.dataquery import (
    DataSourceCreate,
    DataSourceUpdate,
    DataSourceResponse,
    DataSourceListResponse,
    DataSourceTestRequest,
    TableMetadataResponse,
    TableDescriptionUpdate,
)
from app.schemas.system.user import UserResponse
from app.crud.dataquery import datasource as ds_crud
from app.api.auth.auth import get_current_user
from app.core.log_decorator import log_operation
from app.services import db_connector
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dataquery/datasources", tags=["数据源管理"])


@router.get("", response_model=DataSourceListResponse)
async def list_datasources(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="数据源名称"),
    db_type: Optional[str] = Query(None, description="数据库类型"),
    status: Optional[str] = Query(None, description="状态"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取数据源列表"""
    skip = (page - 1) * page_size
    datasources, total = await ds_crud.get_datasources(
        db, skip=skip, limit=page_size, name=name, db_type=db_type, status=status
    )
    return DataSourceListResponse(
        code=200,
        message="success",
        data=[DataSourceResponse.model_validate(ds) for ds in datasources],
        total=total,
    )


@router.get("/{datasource_id}", response_model=DataSourceResponse)
async def get_datasource(
    datasource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取数据源详情"""
    ds = await ds_crud.get_datasource(db, datasource_id)
    if not ds:
        raise HTTPException(status_code=404, detail="数据源不存在")
    return ds


@router.post("", response_model=DataSourceResponse)
@log_operation(module="智能问数-数据源", action="创建数据源", description="创建数据源连接")
async def create_datasource(
    data: DataSourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """创建数据源"""
    password_encrypted = db_connector.encrypt_password(data.password)
    ds = await ds_crud.create_datasource(
        db, data, password_encrypted=password_encrypted, created_by=current_user.username
    )
    return ds


@router.put("/{datasource_id}", response_model=DataSourceResponse)
@log_operation(module="智能问数-数据源", action="更新数据源", description="更新数据源信息")
async def update_datasource(
    datasource_id: int,
    data: DataSourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """更新数据源"""
    password_encrypted = None
    if data.password:
        password_encrypted = db_connector.encrypt_password(data.password)

    ds = await ds_crud.update_datasource(
        db, datasource_id, data, password_encrypted=password_encrypted
    )
    if not ds:
        raise HTTPException(status_code=404, detail="数据源不存在")
    return ds


@router.delete("/{datasource_id}")
@log_operation(module="智能问数-数据源", action="删除数据源", description="删除数据源连接")
async def delete_datasource(
    datasource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """删除数据源"""
    # 关闭连接池
    await db_connector.close_pool(datasource_id)
    success = await ds_crud.delete_datasource(db, datasource_id)
    if not success:
        raise HTTPException(status_code=404, detail="数据源不存在")
    return {"code": 200, "message": "删除成功"}


@router.post("/{datasource_id}/test")
async def test_datasource_connection(
    datasource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """测试已保存的数据源连接"""
    ds = await ds_crud.get_datasource(db, datasource_id)
    if not ds:
        raise HTTPException(status_code=404, detail="数据源不存在")

    password = db_connector.decrypt_password(ds.password_encrypted)
    result = await db_connector.test_connection(
        db_type=ds.db_type,
        host=ds.host,
        port=ds.port,
        username=ds.username,
        password=password,
        database=ds.database,
    )
    return {"code": 200 if result["success"] else 500, "message": result["message"]}


@router.post("/test-connection")
async def test_connection_direct(
    request: DataSourceTestRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """直接测试数据库连接（未保存的数据源）"""
    result = await db_connector.test_connection(
        db_type=request.db_type,
        host=request.host,
        port=request.port,
        username=request.username,
        password=request.password,
        database=request.database,
    )
    return {"code": 200 if result["success"] else 500, "message": result["message"]}


# ============ 表元数据相关 ============


@router.post("/{datasource_id}/sync-metadata")
@log_operation(module="智能问数-数据源", action="同步元数据", description="同步数据源表结构")
async def sync_metadata(
    datasource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """同步数据源的表结构元数据"""
    ds = await ds_crud.get_datasource(db, datasource_id)
    if not ds:
        raise HTTPException(status_code=404, detail="数据源不存在")

    try:
        # 获取远端表结构
        tables = await db_connector.fetch_table_metadata(ds)

        # 获取样例数据
        synced_count = 0
        for table_info in tables:
            sample = await db_connector.fetch_sample_data(
                ds, table_info["table_name"], limit=3
            )
            await ds_crud.upsert_table_metadata(
                db=db,
                datasource_id=datasource_id,
                table_name=table_info["table_name"],
                table_comment=table_info.get("table_comment"),
                columns=table_info.get("columns", []),
                sample_data=sample,
            )
            synced_count += 1

        return {
            "code": 200,
            "message": f"同步完成，共 {synced_count} 张表",
            "data": {"table_count": synced_count},
        }
    except Exception as e:
        logger.error(f"同步元数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")


@router.get("/{datasource_id}/tables")
async def get_tables(
    datasource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取数据源的表列表及元数据"""
    ds = await ds_crud.get_datasource(db, datasource_id)
    if not ds:
        raise HTTPException(status_code=404, detail="数据源不存在")

    tables = await ds_crud.get_table_metadata_list(db, datasource_id)
    return {
        "code": 200,
        "message": "success",
        "data": [TableMetadataResponse.model_validate(t) for t in tables],
    }


@router.put("/{datasource_id}/tables/{table_name}/description")
async def update_table_description(
    datasource_id: int,
    table_name: str,
    data: TableDescriptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """更新表的自定义描述"""
    meta = await ds_crud.update_table_description(
        db, datasource_id, table_name, data.custom_description
    )
    if not meta:
        raise HTTPException(status_code=404, detail="表元数据不存在，请先同步")
    return {"code": 200, "message": "更新成功"}
