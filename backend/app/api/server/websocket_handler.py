"""WebSocket SSH 终端"""

import asyncio
import json
import logging
import websockets
from typing import Optional
from app.services.ssh_service import SSHConnection

logger = logging.getLogger(__name__)

# 存储活跃的 SSH 连接
active_connections: dict[str, SSHConnection] = {}


async def ssh_websocket_handler(websocket):
    """处理 WebSocket SSH 连接（新版 websockets API）"""
    connection_id = None
    
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            
            if action == "connect":
                # 建立 SSH 连接
                connection_id = data.get("connection_id")
                ssh_conn = SSHConnection(
                    hostname=data["hostname"],
                    port=data.get("port", 22),
                    username=data["username"],
                    password=data.get("password"),
                    private_key=data.get("private_key"),
                )
                ssh_conn.connect()
                channel = ssh_conn.open_shell()
                active_connections[connection_id] = ssh_conn
                
                # 启动读取线程
                asyncio.create_task(read_ssh_output(channel, websocket))
                
                await websocket.send(json.dumps({
                    "type": "connected",
                    "message": "SSH 连接成功"
                }))
                
            elif action == "input" and connection_id:
                # 发送输入到 SSH
                if connection_id in active_connections:
                    channel = active_connections[connection_id].channel
                    if channel:
                        channel.send(data.get("data", ""))
                        
            elif action == "resize" and connection_id:
                # 调整终端大小
                if connection_id in active_connections:
                    channel = active_connections[connection_id].channel
                    if channel:
                        channel.resize_pty(
                            width=data.get("cols", 80),
                            height=data.get("rows", 24),
                        )
                        
            elif action == "disconnect" and connection_id:
                # 断开连接
                if connection_id in active_connections:
                    active_connections[connection_id].close()
                    del active_connections[connection_id]
                    await websocket.send(json.dumps({
                        "type": "disconnected",
                        "message": "SSH 连接已关闭"
                    }))
                    
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"WebSocket 连接关闭: {connection_id}")
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
        if connection_id and connection_id in active_connections:
            active_connections[connection_id].close()
            del active_connections[connection_id]


async def read_ssh_output(channel, websocket):
    """读取 SSH 输出并发送到 WebSocket"""
    try:
        while True:
            if channel.recv_ready():
                output = channel.recv(4096).decode("utf-8", errors="ignore")
                await websocket.send(json.dumps({
                    "type": "output",
                    "data": output
                }))
            await asyncio.sleep(0.01)
    except Exception as e:
        logger.error(f"读取 SSH 输出错误: {e}")


def start_websocket_server(host: str = "0.0.0.0", port: int = 8765):
    """启动 WebSocket 服务器"""
    logger.info(f"WebSocket SSH 服务器启动: ws://{host}:{port}")
    
    # 使用新版 websockets API
    async def main():
        async with websockets.serve(ssh_websocket_handler, host, port) as server:
            logger.info(f"WebSocket 服务器运行中: ws://{host}:{port}")
            await asyncio.Future()  # 永久运行
    
    asyncio.run(main())
