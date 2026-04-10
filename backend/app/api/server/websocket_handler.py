"""WebSocket SSH 终端"""

import asyncio
import json
import logging
import websockets

logger = logging.getLogger(__name__)

async def ssh_websocket_handler(websocket):
    """处理 WebSocket 请求（已改为通过 JumpServer 管理终端）。"""
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "connect":
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "内置 Paramiko 终端已下线，请使用 JumpServer Web 终端。"
                }))

    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket 连接关闭")
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")


def start_websocket_server(host: str = "0.0.0.0", port: int = 8765):
    """启动 WebSocket 服务器"""
    logger.info(f"WebSocket SSH 服务器启动: ws://{host}:{port}")
    
    # 使用新版 websockets API
    async def main():
        async with websockets.serve(ssh_websocket_handler, host, port) as server:
            logger.info(f"WebSocket 服务器运行中: ws://{host}:{port}")
            await asyncio.Future()  # 永久运行
    
    asyncio.run(main())
