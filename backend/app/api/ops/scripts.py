"""脚本管理 API 路由"""

import base64
import difflib
import os
import time
import shutil
from pathlib import PurePosixPath
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.schemas.script import (
    ScriptCreate,
    ScriptUpdate,
    ScriptResponse,
    ScriptListResponse,
    ScriptTestRequest,
    ScriptDistributeRequest,
    ScriptVersionResponse,
    ScriptVersionDetailResponse,
    ScriptVersionListResponse,
    ScriptRollbackRequest,
    ScriptVersionDiffResponse,
)
from app.schemas.system.user import UserResponse
from app.crud.ops import script as script_crud
from app.crud.ops import server as server_crud
from app.api.auth.auth import get_current_user
from app.core.log_decorator import log_operation
from app.services.salt_service import salt_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ops/scripts", tags=["脚本管理"])

SCRIPT_STORAGE_DIR = Path(__file__).resolve().parents[3] / "storage" / "scripts"


def _infer_script_type(file_name: str) -> str:
    return "python" if file_name.lower().endswith(".py") else "shell"


def _read_script_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _sanitize_storage_filename(
    upload_file_name: str,
    fallback_stem: str,
    forced_ext: Optional[str] = None,
) -> str:
    raw_name = Path(upload_file_name or "").name
    stem = Path(raw_name).stem or fallback_stem or "script"
    suffix = forced_ext or Path(raw_name).suffix or ".sh"

    safe_stem = "".join(
        ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in stem
    ).strip("._")
    if not safe_stem:
        safe_stem = "script"

    if not suffix.startswith("."):
        suffix = f".{suffix}"
    safe_suffix = "".join(ch for ch in suffix if ch.isalnum() or ch in {".", "_", "-"})
    if safe_suffix in {"", ".", ".."}:
        safe_suffix = ".sh"

    return f"{safe_stem}{safe_suffix}"


def _build_storage_path(file_name: str) -> Path:
    candidate = SCRIPT_STORAGE_DIR / file_name
    if not candidate.exists():
        return candidate

    stem = Path(file_name).stem
    suffix = Path(file_name).suffix
    return SCRIPT_STORAGE_DIR / f"{stem}_{time.time_ns()}{suffix}"


def _to_script_response(script, include_content: bool = False) -> ScriptResponse:
    file_path = script.content or ""
    # Avoid async lazy-load in response serialization (MissingGreenlet)
    project_rel = getattr(script, "__dict__", {}).get("project")
    group_rel = getattr(script, "__dict__", {}).get("group")
    return ScriptResponse(
        id=script.id,
        name=script.name,
        project_id=script.project_id,
        group_id=script.group_id,
        project_name=getattr(project_rel, "name", None) if project_rel is not None else None,
        group_name=getattr(group_rel, "name", None) if group_rel is not None else None,
        description=script.description,
        script_type=script.script_type,
        parameters=script.parameters,
        timeout=script.timeout,
        file_path=file_path,
        source_file_name=Path(file_path).name if file_path else None,
        content=_read_script_file(file_path) if include_content else "",
        created_by=script.created_by,
        created_at=script.created_at,
        updated_at=script.updated_at,
    )


def _to_script_version_response(version, include_content: bool = False) -> ScriptVersionResponse:
    payload = {
        "id": version.id,
        "script_id": version.script_id,
        "version_no": version.version_no,
        "file_path": version.file_path,
        "source_file_name": version.source_file_name,
        "note": version.note,
        "created_by": version.created_by,
        "created_at": version.created_at,
    }
    if include_content:
        return ScriptVersionDetailResponse(
            **payload,
            content=_read_script_file(version.file_path),
        )
    return ScriptVersionResponse(**payload)


@router.get("", response_model=ScriptListResponse)
async def list_scripts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="脚本名称"),
    script_type: Optional[str] = Query(None, description="脚本类型"),
    project_id: Optional[int] = Query(None, description="所属项目ID"),
    group_id: Optional[int] = Query(None, description="所属分组ID"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取脚本列表"""
    skip = (page - 1) * page_size
    scripts, total = await script_crud.get_scripts(
        db,
        skip=skip,
        limit=page_size,
        name=name,
        script_type=script_type,
        project_id=project_id,
        group_id=group_id,
    )
    
    return ScriptListResponse(
        code=200,
        message="success",
        data=[_to_script_response(s, include_content=False) for s in scripts],
        total=total,
    )


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(
    script_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取脚本详情"""
    script = await script_crud.get_script(db, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")
    return _to_script_response(script, include_content=True)


@router.post("", response_model=ScriptResponse)
@log_operation(module="运维-脚本", action="创建脚本", description="创建脚本记录")
async def create_script(
    script: ScriptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """已禁用手工创建，请使用上传接口"""
    raise HTTPException(status_code=400, detail="请使用上传方式创建脚本")


@router.post("/upload", response_model=ScriptResponse)
@log_operation(module="运维-脚本", action="上传脚本", description="上传脚本文件并创建记录")
async def upload_script(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    script_type: Optional[str] = Form(None),
    project_id: Optional[int] = Form(None),
    group_id: Optional[int] = Form(None),
    timeout: int = Form(300),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """上传脚本文件并创建脚本记录"""
    target_path: Optional[Path] = None
    try:
        raw = await file.read()
        if not raw:
            raise HTTPException(status_code=400, detail="上传文件为空")

        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="仅支持 UTF-8 文本脚本文件")

        file_name = file.filename or "script.sh"
        guessed_type = _infer_script_type(file_name)
        final_name = name or (os.path.splitext(file_name)[0] or "script")

        SCRIPT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        ext = ".py" if (script_type or guessed_type) == "python" else ".sh"
        storage_file_name = _sanitize_storage_filename(
            upload_file_name=file_name,
            fallback_stem=final_name,
            forced_ext=ext,
        )
        target_path = _build_storage_path(storage_file_name)
        target_path.write_text(content, encoding="utf-8")

        script_in = ScriptCreate(
            name=final_name,
            project_id=project_id,
            group_id=group_id,
            description=description,
            file_path=str(target_path),
            script_type=script_type or guessed_type,
            timeout=timeout,
        )
        db_script = await script_crud.create_script(
            db, script_in, created_by=current_user.username
        )
    except ValueError as exc:
        if target_path and target_path.exists():
            try:
                target_path.unlink()
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("脚本上传失败: %s", exc)
        if target_path and target_path.exists():
            try:
                target_path.unlink()
            except Exception:
                pass
        raise HTTPException(status_code=500, detail="脚本上传失败，请查看后端日志")

    fresh_script = await script_crud.get_script(db, db_script.id)
    if not fresh_script:
        raise HTTPException(status_code=500, detail="脚本创建后读取失败")
    return _to_script_response(fresh_script, include_content=True)


@router.post("/{script_id}/upload", response_model=ScriptResponse)
@log_operation(module="运维-脚本", action="替换脚本文件", description="重新上传脚本文件")
async def replace_script_file(
    script_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """重新上传脚本文件（更新脚本内容来源路径）"""
    script = await script_crud.get_script(db, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="上传文件为空")
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="仅支持 UTF-8 文本脚本文件")

    SCRIPT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".py" if script.script_type == "python" else ".sh"
    storage_file_name = _sanitize_storage_filename(
        upload_file_name=file.filename or "",
        fallback_stem=script.name,
        forced_ext=ext,
    )
    target_path = _build_storage_path(storage_file_name)
    target_path.write_text(content, encoding="utf-8")

    updated = await script_crud.update_script(
        db,
        script_id,
        ScriptUpdate(file_path=str(target_path)),
        updated_by=current_user.username,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="脚本不存在")

    fresh_script = await script_crud.get_script(db, updated.id)
    if not fresh_script:
        raise HTTPException(status_code=500, detail="脚本更新后读取失败")
    return _to_script_response(fresh_script, include_content=True)


@router.put("/{script_id}", response_model=ScriptResponse)
@log_operation(module="运维-脚本", action="更新脚本", description="更新脚本基础信息")
async def update_script(
    script_id: int,
    script: ScriptUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """更新脚本"""
    try:
        db_script = await script_crud.update_script(
            db,
            script_id,
            script,
            updated_by=current_user.username,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not db_script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    fresh_script = await script_crud.get_script(db, db_script.id)
    if not fresh_script:
        raise HTTPException(status_code=500, detail="脚本更新后读取失败")
    return _to_script_response(fresh_script, include_content=True)


@router.get("/{script_id}/versions", response_model=ScriptVersionListResponse)
async def list_script_versions(
    script_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    script = await script_crud.get_script(db, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    versions = await script_crud.list_script_versions(db, script_id)
    return ScriptVersionListResponse(
        code=200,
        message="success",
        data=[_to_script_version_response(item, include_content=False) for item in versions],
    )


@router.get("/{script_id}/versions/compare", response_model=ScriptVersionDiffResponse)
async def compare_script_versions(
    script_id: int,
    from_version_id: int = Query(..., description="起始版本ID"),
    to_version_id: int = Query(..., description="目标版本ID"),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    if from_version_id == to_version_id:
        raise HTTPException(status_code=400, detail="请选择两个不同版本进行对比")

    from_version = await script_crud.get_script_version(db, script_id, from_version_id)
    to_version = await script_crud.get_script_version(db, script_id, to_version_id)
    if not from_version or not to_version:
        raise HTTPException(status_code=404, detail="版本不存在")

    from_lines = _read_script_file(from_version.file_path).splitlines()
    to_lines = _read_script_file(to_version.file_path).splitlines()
    diff_text = "\n".join(
        difflib.unified_diff(
            from_lines,
            to_lines,
            fromfile=f"v{from_version.version_no}",
            tofile=f"v{to_version.version_no}",
            lineterm="",
        )
    )

    return ScriptVersionDiffResponse(
        code=200,
        message="success",
        from_version_id=from_version_id,
        to_version_id=to_version_id,
        diff=diff_text,
    )


@router.get("/{script_id}/versions/{version_id}", response_model=ScriptVersionDetailResponse)
async def get_script_version_detail(
    script_id: int,
    version_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    version = await script_crud.get_script_version(db, script_id, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="版本不存在")
    return _to_script_version_response(version, include_content=True)


@router.post("/{script_id}/rollback", response_model=ScriptResponse)
@log_operation(module="运维-脚本", action="回滚脚本版本", description="回滚到指定脚本版本")
async def rollback_script(
    script_id: int,
    payload: ScriptRollbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    script = await script_crud.get_script(db, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    version = await script_crud.get_script_version(db, script_id, payload.version_id)
    if not version:
        raise HTTPException(status_code=404, detail="目标版本不存在")

    source_path = Path(version.file_path)
    if not source_path.exists():
        raise HTTPException(status_code=400, detail="目标版本文件不存在，无法回滚")

    SCRIPT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    suffix = source_path.suffix or (".py" if script.script_type == "python" else ".sh")
    storage_file_name = _sanitize_storage_filename(
        upload_file_name=version.source_file_name or source_path.name,
        fallback_stem=f"{script.name}_rollback_v{version.version_no}",
        forced_ext=suffix,
    )
    target_path = _build_storage_path(storage_file_name)
    shutil.copy2(source_path, target_path)

    final_note = payload.note or f"回滚到 v{version.version_no}"
    script_type = "python" if suffix.lower() == ".py" else "shell"
    updated = await script_crud.rollback_script_to_file(
        db,
        script_id=script_id,
        file_path=str(target_path),
        source_file_name=version.source_file_name or source_path.name,
        note=final_note,
        updated_by=current_user.username,
        script_type=script_type,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="脚本不存在")

    fresh_script = await script_crud.get_script(db, updated.id)
    if not fresh_script:
        raise HTTPException(status_code=500, detail="脚本回滚后读取失败")
    return _to_script_response(fresh_script, include_content=True)


@router.delete("/{script_id}")
@log_operation(module="运维-脚本", action="删除脚本", description="删除脚本记录")
async def delete_script(
    script_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
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
    current_user: UserResponse = Depends(get_current_user),
):
    """测试执行脚本"""
    # 获取脚本
    script = await script_crud.get_script(db, request.script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")
    
    # TODO: 实现脚本测试执行
    # 1. 获取服务器信息
    # 2. 替换脚本中的参数
    # 3. 执行脚本 (JumpServer 或 Salt)
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


@router.post("/{script_id}/distribute")
@log_operation(module="运维-脚本", action="分发脚本", description="通过 SaltStack 分发脚本")
async def distribute_script(
    script_id: int,
    request: ScriptDistributeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """通过 SaltStack 分发脚本到目标服务器目录"""
    script = await script_crud.get_script(db, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    suffix = ".py" if script.script_type == "python" else ".sh"
    default_file_name = Path(script.content or "").name or f"{script.name}{suffix}"
    raw_file_name = request.file_name or default_file_name
    safe_file_name = os.path.basename(raw_file_name)
    if not safe_file_name:
        raise HTTPException(status_code=400, detail="非法文件名")

    target_dir = request.target_directory.strip()
    if not target_dir:
        raise HTTPException(status_code=400, detail="目标目录不能为空")

    remote_path = str(PurePosixPath(target_dir) / safe_file_name)
    script_text = _read_script_file(script.content or "")
    if not script_text:
        raise HTTPException(status_code=400, detail="脚本文件内容为空或文件不存在，请重新上传脚本")
    script_b64 = base64.b64encode(script_text.encode("utf-8")).decode("ascii")
    push_cmd = (
        f"mkdir -p '{target_dir}' && "
        f"printf '%s' '{script_b64}' | base64 -d > '{remote_path}' && "
        f"chmod +x '{remote_path}'"
    )

    results = []
    success_count = 0
    for server_id in request.server_ids:
        server = await server_crud.get_server(db, server_id)
        if not server:
            results.append({"server_id": server_id, "success": False, "message": "服务器不存在"})
            continue

        target = server.salt_minion_id or server.hostname
        if not target:
            results.append({
                "server_id": server_id,
                "success": False,
                "message": "缺少 salt_minion_id 或 hostname",
            })
            continue

        try:
            salt_result = await salt_service.run_command(
                env_name=server.environment,
                target=target,
                fun="cmd.run_all",
                arg=[push_cmd],
            )
            ret = salt_result.get("return", []) if isinstance(salt_result, dict) else []
            ret_map = ret[0] if ret and isinstance(ret[0], dict) else {}
            output = ret_map.get(target)

            retcode = None
            stderr = ""
            stdout = ""
            if isinstance(output, dict):
                retcode = output.get("retcode")
                stderr = str(output.get("stderr") or "")
                stdout = str(output.get("stdout") or "")
                ok = retcode == 0
            else:
                output_text = str(output or "")
                ok = bool(output) and "Traceback" not in output_text
                stdout = output_text

            error_message = stderr.strip() or stdout.strip() or "分发执行返回异常"
            if ok:
                success_count += 1
            results.append(
                {
                    "server_id": server.id,
                    "server_name": server.name,
                    "target": target,
                    "success": ok,
                    "message": "分发成功" if ok else error_message,
                    "output": output,
                    "retcode": retcode,
                    "remote_path": remote_path,
                }
            )
        except Exception as e:
            logger.error(f"脚本分发失败 server_id={server.id}: {e}")
            results.append(
                {
                    "server_id": server.id,
                    "server_name": server.name,
                    "target": target,
                    "success": False,
                    "message": str(e),
                    "remote_path": remote_path,
                }
            )

    all_success = success_count == len(request.server_ids)
    return {
        "code": 200 if all_success else 207,
        "message": f"分发完成: 成功 {success_count}/{len(request.server_ids)}",
        "data": {
            "script_id": script.id,
            "script_name": script.name,
            "remote_path": remote_path,
            "results": results,
        },
    }
