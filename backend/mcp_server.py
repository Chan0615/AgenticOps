#!/usr/bin/env python3
"""
AgenticOps MCP Server

基于 Model Context Protocol (MCP) 的运维工具服务器。
Claude Desktop、Cursor 等支持 MCP 的 AI 工具可以通过此服务器
直接与 AgenticOps 运维平台交互。

运行模式：stdio（本地内网使用）

启动方式：
    python backend/mcp_server.py

Claude Desktop 配置（claude_desktop_config.json）：
    {
      "mcpServers": {
        "agenticops": {
          "command": "python",
          "args": ["D:\\\\path\\\\to\\\\AgenticOps\\\\backend\\\\mcp_server.py"],
          "env": {
            "CONFIG_FILE": "D:\\\\path\\\\to\\\\AgenticOps\\\\backend\\\\config.yaml"
          }
        }
      }
    }

依赖安装：
    pip install mcp
"""

import sys
import os
import asyncio
import json
import logging

# 确保 backend 目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def _check_mcp_installed():
    try:
        import mcp
        return True
    except ImportError:
        print(
            "❌ 缺少 mcp 库，请先安装：\n\n"
            "    pip install mcp\n\n"
            "然后重新启动 MCP Server。",
            file=sys.stderr,
        )
        sys.exit(1)


_check_mcp_installed()

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
    ListToolsResult,
)


# ============ 初始化数据库连接 ============

async def _get_db_session():
    """获取异步数据库 session"""
    from app.db.database import AsyncSessionLocal
    return AsyncSessionLocal()


# ============ MCP Server 定义 ============

server = Server("agenticops")


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """列出所有可用工具"""
    from app.rag.tools import get_ops_tools_schema

    tools_schema = get_ops_tools_schema()
    # 加入基础工具
    base_tools = [
        Tool(
            name="get_current_time",
            description="获取当前系统时间（日期、时间、星期）",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="parse_cron_expression",
            description="解释 Cron 表达式的中文含义",
            inputSchema={
                "type": "object",
                "properties": {
                    "cron_expression": {"type": "string", "description": "5段Cron表达式，如 '0 9 * * 1-5'"},
                },
                "required": ["cron_expression"],
            },
        ),
        Tool(
            name="convert_natural_language_to_cron",
            description="将自然语言转换为 Cron 表达式，如'每天18:30'→'30 18 * * *'",
            inputSchema={
                "type": "object",
                "properties": {
                    "natural_text": {"type": "string", "description": "自然语言描述，如'每天18:30'"},
                },
                "required": ["natural_text"],
            },
        ),
    ]

    ops_tools = [
        Tool(
            name=t["function"]["name"],
            description=t["function"]["description"],
            inputSchema=t["function"]["parameters"],
        )
        for t in tools_schema
    ]

    return ListToolsResult(tools=base_tools + ops_tools)


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """执行工具调用"""
    from app.rag.tools import (
        get_current_time,
        parse_cron_expression,
        convert_natural_language_to_cron,
        WRITE_OP_TOOL_NAMES,
        make_ops_tools,
    )

    # 基础工具（无需 db）
    if name == "get_current_time":
        result = get_current_time.invoke({})
        return CallToolResult(content=[TextContent(type="text", text=result)])

    if name == "parse_cron_expression":
        result = parse_cron_expression.invoke(arguments)
        return CallToolResult(content=[TextContent(type="text", text=result)])

    if name == "convert_natural_language_to_cron":
        result = convert_natural_language_to_cron.invoke(arguments)
        return CallToolResult(content=[TextContent(type="text", text=result)])

    # 运维工具（需要 db）
    db = await _get_db_session()
    try:
        async with db as session:
            ops_tools = make_ops_tools(session)
            ops_tool_map = {fn.__name__: fn for fn in ops_tools}

            if name not in ops_tool_map:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"未知工具：{name}")],
                    isError=True,
                )

            # 写操作工具在 MCP 模式下添加明显警告提示
            if name in WRITE_OP_TOOL_NAMES:
                warning = (
                    f"⚠️ **写操作警告**：工具 `{name}` 将在真实环境中执行操作。\n"
                    f"参数：{json.dumps(arguments, ensure_ascii=False, indent=2)}\n\n"
                    "正在执行...\n\n"
                )
                tool_fn = ops_tool_map[name]
                result = await tool_fn(**arguments)
                return CallToolResult(
                    content=[TextContent(type="text", text=warning + str(result))]
                )

            tool_fn = ops_tool_map[name]
            result = await tool_fn(**arguments)
            return CallToolResult(
                content=[TextContent(type="text", text=str(result))]
            )
    except Exception as e:
        logger.error(f"[MCP] 工具执行失败 {name}: {e}", exc_info=True)
        return CallToolResult(
            content=[TextContent(type="text", text=f"工具执行失败：{e}")],
            isError=True,
        )


# ============ 主入口 ============

async def main():
    """启动 MCP stdio 服务器"""
    logger.info("AgenticOps MCP Server 启动中...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
