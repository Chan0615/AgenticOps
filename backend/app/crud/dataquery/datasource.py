"""数据源 CRUD 操作"""

from typing import List, Optional
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dataquery import DataSource, TableMetadata
from app.schemas.dataquery import DataSourceCreate, DataSourceUpdate
import logging

logger = logging.getLogger(__name__)


async def get_datasource(db: AsyncSession, datasource_id: int) -> Optional[DataSource]:
    """根据ID获取数据源"""
    result = await db.execute(select(DataSource).where(DataSource.id == datasource_id))
    return result.scalar_one_or_none()


async def get_datasources(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = None,
    db_type: Optional[str] = None,
    status: Optional[str] = None,
) -> tuple[List[DataSource], int]:
    """获取数据源列表"""
    query = select(DataSource)
    count_query = select(func.count(DataSource.id))

    if name:
        query = query.where(DataSource.name.ilike(f"%{name}%"))
        count_query = count_query.where(DataSource.name.ilike(f"%{name}%"))
    if db_type:
        query = query.where(DataSource.db_type == db_type)
        count_query = count_query.where(DataSource.db_type == db_type)
    if status:
        query = query.where(DataSource.status == status)
        count_query = count_query.where(DataSource.status == status)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset(skip).limit(limit).order_by(DataSource.created_at.desc())
    result = await db.execute(query)
    datasources = result.scalars().all()

    return datasources, total


async def create_datasource(
    db: AsyncSession,
    data: DataSourceCreate,
    password_encrypted: str,
    created_by: str = None,
) -> DataSource:
    """创建数据源"""
    db_ds = DataSource(
        name=data.name,
        description=data.description,
        db_type=data.db_type,
        host=data.host,
        port=data.port,
        database=data.database,
        username=data.username,
        password_encrypted=password_encrypted,
        is_system_db=data.is_system_db,
        extra_config=data.extra_config,
        created_by=created_by,
    )
    db.add(db_ds)
    await db.commit()
    await db.refresh(db_ds)
    return db_ds


async def update_datasource(
    db: AsyncSession,
    datasource_id: int,
    data: DataSourceUpdate,
    password_encrypted: Optional[str] = None,
) -> Optional[DataSource]:
    """更新数据源"""
    db_ds = await get_datasource(db, datasource_id)
    if not db_ds:
        return None

    update_data = data.model_dump(exclude_unset=True)
    # password 字段由外层处理为 password_encrypted
    update_data.pop("password", None)
    for field, value in update_data.items():
        setattr(db_ds, field, value)
    if password_encrypted is not None:
        db_ds.password_encrypted = password_encrypted

    await db.commit()
    await db.refresh(db_ds)
    return db_ds


async def delete_datasource(db: AsyncSession, datasource_id: int) -> bool:
    """删除数据源"""
    db_ds = await get_datasource(db, datasource_id)
    if not db_ds:
        return False
    await db.delete(db_ds)
    await db.commit()
    return True


# ============ 表元数据 ============


async def get_table_metadata_list(
    db: AsyncSession, datasource_id: int
) -> List[TableMetadata]:
    """获取数据源的所有表元数据"""
    result = await db.execute(
        select(TableMetadata)
        .where(TableMetadata.datasource_id == datasource_id)
        .order_by(TableMetadata.table_name)
    )
    return result.scalars().all()


async def get_table_metadata_by_name(
    db: AsyncSession, datasource_id: int, table_name: str
) -> Optional[TableMetadata]:
    """根据表名获取元数据"""
    result = await db.execute(
        select(TableMetadata).where(
            TableMetadata.datasource_id == datasource_id,
            TableMetadata.table_name == table_name,
        )
    )
    return result.scalar_one_or_none()


async def upsert_table_metadata(
    db: AsyncSession,
    datasource_id: int,
    table_name: str,
    table_comment: Optional[str],
    columns: list,
    sample_data: Optional[list] = None,
) -> TableMetadata:
    """创建或更新表元数据"""
    from sqlalchemy.sql import func as sqlfunc

    existing = await get_table_metadata_by_name(db, datasource_id, table_name)
    if existing:
        existing.table_comment = table_comment
        existing.columns = columns
        existing.sample_data = sample_data
        existing.synced_at = sqlfunc.now()
        await db.commit()
        await db.refresh(existing)
        return existing

    meta = TableMetadata(
        datasource_id=datasource_id,
        table_name=table_name,
        table_comment=table_comment,
        columns=columns,
        sample_data=sample_data,
    )
    db.add(meta)
    await db.commit()
    await db.refresh(meta)
    return meta


async def update_table_description(
    db: AsyncSession,
    datasource_id: int,
    table_name: str,
    custom_description: str,
) -> Optional[TableMetadata]:
    """更新表自定义描述"""
    meta = await get_table_metadata_by_name(db, datasource_id, table_name)
    if not meta:
        return None
    meta.custom_description = custom_description
    await db.commit()
    await db.refresh(meta)
    return meta


async def clear_table_metadata(db: AsyncSession, datasource_id: int):
    """清除数据源的所有表元数据"""
    await db.execute(
        delete(TableMetadata).where(TableMetadata.datasource_id == datasource_id)
    )
    await db.commit()
