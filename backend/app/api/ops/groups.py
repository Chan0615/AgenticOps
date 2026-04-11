"""项目与分组管理 API"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.auth import get_current_user
from app.core.log_decorator import log_operation
from app.crud.ops import group as group_crud
from app.db.database import get_db
from app.schemas.group import (
    OpsGroupCreate,
    OpsGroupListResponse,
    OpsGroupResponse,
    OpsGroupUpdate,
    OpsProjectCreate,
    OpsProjectListResponse,
    OpsProjectResponse,
    OpsProjectUpdate,
)
from app.schemas.system.user import UserResponse

router = APIRouter(tags=["项目与分组"])


@router.get("/api/ops/projects", response_model=OpsProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页数量"),
    name: Optional[str] = Query(None, description="项目名称"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    skip = (page - 1) * page_size
    projects, total = await group_crud.get_projects(
        db,
        skip=skip,
        limit=page_size,
        name=name,
    )
    return OpsProjectListResponse(
        code=200,
        message="success",
        data=[OpsProjectResponse.model_validate(p) for p in projects],
        total=total,
    )


@router.post("/api/ops/projects", response_model=OpsProjectResponse)
@log_operation(module="运维-分组", action="创建项目", description="创建运维项目")
async def create_project(
    project: OpsProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return await group_crud.create_project(db, project, created_by=current_user.username)


@router.put("/api/ops/projects/{project_id}", response_model=OpsProjectResponse)
@log_operation(module="运维-分组", action="更新项目", description="更新运维项目")
async def update_project(
    project_id: int,
    project: OpsProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    db_project = await group_crud.update_project(db, project_id, project)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_project


@router.delete("/api/ops/projects/{project_id}")
@log_operation(module="运维-分组", action="删除项目", description="删除运维项目")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        success = await group_crud.delete_project(db, project_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not success:
        raise HTTPException(status_code=404, detail="项目不存在")
    return {"code": 200, "message": "删除成功"}


@router.get("/api/ops/groups", response_model=OpsGroupListResponse)
async def list_groups(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(200, ge=1, le=500, description="每页数量"),
    project_id: Optional[int] = Query(None, description="所属项目ID"),
    name: Optional[str] = Query(None, description="分组名称"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    skip = (page - 1) * page_size
    groups, total = await group_crud.get_groups(
        db,
        skip=skip,
        limit=page_size,
        project_id=project_id,
        name=name,
    )

    data = []
    for g in groups:
        item = OpsGroupResponse.model_validate(g)
        item.project_name = getattr(g.project, "name", None) if getattr(g, "project", None) else None
        data.append(item)

    return OpsGroupListResponse(
        code=200,
        message="success",
        data=data,
        total=total,
    )


@router.post("/api/ops/groups", response_model=OpsGroupResponse)
@log_operation(module="运维-分组", action="创建分组", description="创建运维分组")
async def create_group(
    group: OpsGroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        db_group = await group_crud.create_group(db, group, created_by=current_user.username)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    result = OpsGroupResponse.model_validate(db_group)
    project = await group_crud.get_project(db, db_group.project_id)
    result.project_name = project.name if project else None
    return result


@router.put("/api/ops/groups/{group_id}", response_model=OpsGroupResponse)
@log_operation(module="运维-分组", action="更新分组", description="更新运维分组")
async def update_group(
    group_id: int,
    group: OpsGroupUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        db_group = await group_crud.update_group(db, group_id, group)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not db_group:
        raise HTTPException(status_code=404, detail="分组不存在")

    result = OpsGroupResponse.model_validate(db_group)
    project = await group_crud.get_project(db, db_group.project_id)
    result.project_name = project.name if project else None
    return result


@router.delete("/api/ops/groups/{group_id}")
@log_operation(module="运维-分组", action="删除分组", description="删除运维分组")
async def delete_group(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        success = await group_crud.delete_group(db, group_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not success:
        raise HTTPException(status_code=404, detail="分组不存在")
    return {"code": 200, "message": "删除成功"}
