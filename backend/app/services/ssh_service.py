"""Paramiko SSH 服务层"""

import asyncio
import logging
import paramiko
from typing import Optional
from io import StringIO

logger = logging.getLogger(__name__)


class SSHConnection:
    """SSH 连接管理器"""

    def __init__(
        self,
        hostname: str,
        port: int = 22,
        username: str = "root",
        password: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        self.client: Optional[paramiko.SSHClient] = None
        self.channel = None

    def connect(self) -> bool:
        """建立 SSH 连接"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.private_key:
                # 使用私钥连接
                key = paramiko.RSAKey.from_private_key(StringIO(self.private_key))
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    pkey=key,
                    timeout=10,
                )
            else:
                # 使用密码连接
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=10,
                )

            logger.info(f"SSH 连接成功: {self.hostname}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"SSH 连接失败: {e}")
            raise

    def execute_command(self, command: str) -> dict:
        """执行命令"""
        if not self.client:
            raise Exception("SSH 未连接")

        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=30)
            output = stdout.read().decode("utf-8")
            error = stderr.read().decode("utf-8")
            exit_code = stdout.channel.recv_exit_status()

            return {
                "output": output,
                "error": error,
                "exit_code": exit_code,
            }
        except Exception as e:
            logger.error(f"命令执行失败: {e}")
            raise

    def open_shell(self) -> paramiko.channel.Channel:
        """打开交互式 Shell"""
        if not self.client:
            raise Exception("SSH 未连接")

        self.channel = self.client.invoke_shell()
        return self.channel

    def close(self):
        """关闭连接"""
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
            logger.info(f"SSH 连接已关闭: {self.hostname}")


class SSHManager:
    """SSH 连接池管理器"""

    def __init__(self):
        self.connections: dict[str, SSHConnection] = {}

    def get_connection(
        self,
        server_id: str,
        hostname: str,
        port: int = 22,
        username: str = "root",
        password: Optional[str] = None,
        private_key: Optional[str] = None,
    ) -> SSHConnection:
        """获取或创建 SSH 连接"""
        if server_id not in self.connections:
            conn = SSHConnection(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                private_key=private_key,
            )
            conn.connect()
            self.connections[server_id] = conn
        return self.connections[server_id]

    def remove_connection(self, server_id: str):
        """移除连接"""
        if server_id in self.connections:
            self.connections[server_id].close()
            del self.connections[server_id]

    def close_all(self):
        """关闭所有连接"""
        for conn in self.connections.values():
            conn.close()
        self.connections.clear()


# 全局实例
ssh_manager = SSHManager()
