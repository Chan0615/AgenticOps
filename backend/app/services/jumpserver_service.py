"""JumpServer REST API service."""

import logging
from typing import Any, Optional

import aiohttp

from app.core import config

logger = logging.getLogger(__name__)


class JumpServerService:
    """JumpServer API client."""

    def __init__(self):
        self.base_url = str(config._get("jumpserver", "base_url", default="")).rstrip("/")
        self.org_id = config._get(
            "jumpserver",
            "org_id",
            default="00000000-0000-0000-0000-000000000002",
        )
        self.auth_mode = config._get("jumpserver", "auth_mode", default="private_token")
        self.private_token = config._get("jumpserver", "private_token", default="")
        self.username = config._get("jumpserver", "username", default="")
        self.password = config._get("jumpserver", "password", default="")

    def is_configured(self) -> bool:
        if not self.base_url:
            return False
        if self.auth_mode == "private_token":
            return bool(self.private_token)
        if self.auth_mode == "password":
            return bool(self.username and self.password)
        return False

    async def _get_bearer_token(self) -> str:
        url = f"{self.base_url}/api/v1/authentication/auth/"
        payload = {"username": self.username, "password": self.password}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"JumpServer 登录失败: HTTP {resp.status}")
                data = await resp.json()
                token = data.get("token")
                if not token:
                    raise RuntimeError("JumpServer 登录失败: 响应中缺少 token")
                return token

    async def _build_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-JMS-ORG": self.org_id,
        }

        if self.auth_mode == "private_token":
            headers["Authorization"] = f"Token {self.private_token}"
            return headers

        if self.auth_mode == "password":
            token = await self._get_bearer_token()
            headers["Authorization"] = f"Bearer {token}"
            return headers

        raise RuntimeError(f"不支持的 JumpServer 认证方式: {self.auth_mode}")

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        if not self.is_configured():
            raise RuntimeError("JumpServer 未配置，请先填写 backend/config.yaml 的 jumpserver 配置")

        headers = await self._build_headers()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method.upper(),
                url,
                headers=headers,
                params=params,
                json=data,
            ) as resp:
                body_text = await resp.text()
                if resp.status >= 400:
                    raise RuntimeError(
                        f"JumpServer API 调用失败: {method.upper()} {endpoint} -> HTTP {resp.status}, body={body_text}"
                    )

                if not body_text:
                    return {}

                try:
                    return await resp.json()
                except Exception:
                    return {"raw": body_text}

    async def test_asset_connectivity(self, hostname: str) -> dict[str, Any]:
        """Validate JumpServer auth and asset existence by hostname/IP."""
        candidates = [
            "api/v1/assets/hosts/",
            "api/v1/assets/assets/",
        ]

        last_error: Optional[Exception] = None
        for endpoint in candidates:
            try:
                payload = await self.request("GET", endpoint, params={"search": hostname, "limit": 10})
                if isinstance(payload, dict):
                    items = payload.get("results")
                    if isinstance(items, list):
                        matched = any(
                            hostname in {
                                str(item.get("ip", "")),
                                str(item.get("address", "")),
                                str(item.get("hostname", "")),
                                str(item.get("name", "")),
                            }
                            for item in items
                        )
                        return {
                            "success": matched,
                            "message": "JumpServer 连接成功" if matched else "JumpServer 连接成功，但未找到对应资产",
                            "asset_count": len(items),
                        }
                return {"success": True, "message": "JumpServer 连接成功"}
            except Exception as exc:
                last_error = exc

        if last_error:
            raise last_error
        raise RuntimeError("JumpServer 连通性检查失败")


jumpserver_service = JumpServerService()
