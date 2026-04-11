"""通用操作日志装饰器"""

import functools
import time
import json
import logging
from typing import Optional, Callable, Any
from fastapi import Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.common.log import create_log
from app.core.request_context import get_current_request
from app.core.security import get_current_user_from_request

logger = logging.getLogger(__name__)


def _serialize_for_log(data: Any) -> Any:
    if data is None:
        return None
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json")
    if isinstance(data, dict):
        return data
    if isinstance(data, (list, tuple)):
        return [_serialize_for_log(item) for item in data]
    if isinstance(data, (str, int, float, bool)):
        return data
    if hasattr(data, "dict") and callable(getattr(data, "dict")):
        try:
            return data.dict()
        except Exception:
            return str(data)
    return str(data)


def _extract_user_from_dependency(dep_user: Any) -> tuple[Optional[int], Optional[str]]:
    if not dep_user:
        return None, None
    uid = getattr(dep_user, "id", None)
    uname = getattr(dep_user, "username", None)
    return uid, uname


def _collect_fallback_request_params(kwargs: dict) -> Optional[dict]:
    excluded_keys = {"db", "current_user", "request"}
    payload: dict[str, Any] = {}
    for key, value in kwargs.items():
        if key in excluded_keys:
            continue
        payload[key] = _serialize_for_log(value)
    return payload or None


def log_operation(
    module: str,
    action: str,
    description: Optional[str] = None,
):
    """
    操作日志装饰器
    
    使用示例:
        @router.post("/servers")
        @log_operation(module="服务器管理", action="创建服务器", description="添加新服务器")
        async def create_server(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            # 获取请求对象和数据库会话
            request: Optional[Request] = None
            db: Optional[AsyncSession] = None
            
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                elif hasattr(arg, '__class__') and 'AsyncSession' in str(type(arg)):
                    db = arg
            
            for value in kwargs.values():
                if isinstance(value, Request):
                    request = value
                elif hasattr(value, '__class__') and 'AsyncSession' in str(type(value)):
                    db = value

            if request is None:
                request = get_current_request()
            
            # 获取用户信息
            user_id = None
            username = None
            try:
                if request:
                    user = await get_current_user_from_request(request)
                    if user:
                        user_id = user.id
                        username = user.username
            except Exception as e:
                logger.debug(f"获取用户信息失败: {e}")

            if user_id is None or username is None:
                dep_user = kwargs.get("current_user")
                dep_user_id, dep_username = _extract_user_from_dependency(dep_user)
                user_id = user_id if user_id is not None else dep_user_id
                username = username if username is not None else dep_username
            
            # 获取请求信息
            method = request.method if request else None
            path = request.url.path if request else None
            ip_address = request.client.host if request and request.client else None
            user_agent = request.headers.get("user-agent") if request else None
            
            # 获取请求参数
            request_params = None
            try:
                if request and request.method in ["POST", "PUT", "PATCH"]:
                    body = await request.body()
                    if body:
                        request_params = json.loads(body)
                elif request:
                    request_params = dict(request.query_params)
            except Exception as e:
                logger.debug(f"获取请求参数失败: {e}")

            if request_params is None:
                request_params = _collect_fallback_request_params(kwargs)
            
            status_code = 200
            response_data = None
            error_message = None
            
            try:
                # 执行原函数
                result = await func(*args, **kwargs)
                
                # 获取响应数据
                if isinstance(result, dict):
                    response_data = result
                    status_code = 200
                elif hasattr(result, 'status_code'):
                    status_code = result.status_code
                    response_data = _serialize_for_log(result)
                else:
                    response_data = _serialize_for_log(result)
                
                return result
                
            except HTTPException as e:
                status_code = e.status_code
                error_message = str(e.detail)
                raise
                
            except Exception as e:
                status_code = 500
                error_message = str(e)
                raise
                
            finally:
                # 计算执行时间
                execution_time = int((time.time() - start_time) * 1000)
                
                # 异步记录日志（不阻塞主流程）
                if db:
                    try:
                        await create_log(
                            db=db,
                            module=module,
                            action=action,
                            description=description,
                            user_id=user_id,
                            username=username,
                            method=method,
                            path=path,
                            status_code=status_code,
                            request_params=request_params,
                            response_data=response_data,
                            error_message=error_message,
                            ip_address=ip_address,
                            user_agent=user_agent,
                            execution_time=execution_time,
                        )
                    except Exception as e:
                        logger.error(f"记录操作日志失败: {e}")
        
        return wrapper
    return decorator
