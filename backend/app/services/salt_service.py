"""SaltStack 服务层"""

import asyncio
import logging
from typing import Optional
import aiohttp
from app.core import config

logger = logging.getLogger(__name__)


class SaltService:
    """SaltStack API 服务"""

    def __init__(self):
        self.environments = config._get("saltstack", default={})

    async def _request(
        self,
        env_name: str,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
    ) -> dict:
        """发送 Salt API 请求"""
        env_config = self.environments.get(env_name)
        if not env_config:
            raise ValueError(f"Salt 环境 '{env_name}' 不存在")

        url = f"{env_config['url']}/{endpoint.lstrip('/')}"
        
        # 登录获取 token
        token = await self._login(env_name)
        
        headers = {
            "X-Auth-Token": token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, json=data, headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Salt API 错误: {error_text}")
                return await response.json()

    async def _login(self, env_name: str) -> str:
        """登录 Salt API"""
        env_config = self.environments.get(env_name)
        url = f"{env_config['url']}/login"
        
        data = {
            "username": env_config["salt_name"],
            "password": env_config["salt_pass"],
            "eauth": "pam",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    raise Exception(f"Salt 登录失败")
                result = await response.json()
                return result["return"][0]["token"]

    async def run_command(
        self, env_name: str, target: str, fun: str, arg: list = None
    ) -> dict:
        """执行 Salt 命令"""
        data = {
            "client": "local",
            "tgt": target,
            "fun": fun,
        }
        if arg:
            data["arg"] = arg

        return await self._request(env_name, "POST", "/run", data)

    async def get_minions(self, env_name: str) -> dict:
        """获取 Minion 列表"""
        return await self._request(env_name, "GET", "/minions")

    async def test_ping(self, env_name: str, target: str = "*") -> dict:
        """测试 Minion 连接"""
        return await self.run_command(env_name, target, "test.ping")

    async def get_server_info(self, env_name: str, target: str = "*") -> dict:
        """获取服务器信息"""
        return await self.run_command(env_name, target, "grains.items")

    async def run_shell_command(
        self, env_name: str, target: str, command: str
    ) -> dict:
        """执行 Shell 命令"""
        return await self.run_command(env_name, target, "cmd.run", [command])


# 全局实例
salt_service = SaltService()
