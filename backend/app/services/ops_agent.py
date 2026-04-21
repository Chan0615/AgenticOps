"""
运维 AI 助手核心服务

实现基于 Function Calling 的运维智能对话，支持：
- 只读工具：AI 自主调用，直接返回结果
- 写操作工具：挂起等待用户确认，确认后再执行
- SSE 流式输出
- 多轮对话历史（复用 agent_conversation 表）
"""

import json
import logging
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ai import call_llm
from app.crud.agent import conversation as conv_crud
from app.rag.tools import (
    WRITE_OP_TOOL_NAMES,
    get_ops_tools_schema,
    make_ops_tools,
    parse_cron_expression,
    convert_natural_language_to_cron,
    get_current_time,
    calculate,
)

logger = logging.getLogger(__name__)

# ============ System Prompt ============

OPS_SYSTEM_PROMPT = """你是「AgenticOps 运维助手」，一个智能运维平台内置的 AI 助手。

你可以通过工具帮助用户完成以下运维工作：
- **查询服务器**：列表、状态、环境筛选
- **查询脚本**：搜索脚本库中的脚本
- **查询定时任务**：任务列表、执行频率、启用状态
- **查询执行日志**：查看任务运行历史和结果
- **执行命令**（需用户确认）：在目标服务器上执行 Shell 命令
- **创建定时任务**（需用户确认）：新建调度任务
- **启用/禁用任务**（需用户确认）：修改任务调度状态
- **解析/转换 Cron 表达式**：解释或将自然语言转换为 Cron

工作规范：
1. 优先调用工具获取真实数据，不要凭空捏造信息
2. 对于只读操作（查询、解析），直接调用工具并返回结果
3. 对于写操作（执行命令、创建任务、修改状态），工具描述中有 ⚠️[写操作-需确认] 标记，调用后系统会自动暂停等待用户确认
4. 回答简洁清晰，数据展示时使用 Markdown 格式
5. 遇到不确定的操作，主动询问用户确认信息
6. 如果用户的请求不涉及任何工具，直接文字回答即可

当前时间可通过 get_current_time 工具获取。"""


# ============ 基础工具 Schema（无需 db）============

BASE_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前系统时间。只读操作。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式。只读操作。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "parse_cron_expression",
            "description": "解释 Cron 表达式的含义。只读操作。",
            "parameters": {
                "type": "object",
                "properties": {
                    "cron_expression": {"type": "string", "description": "标准5段Cron表达式"},
                },
                "required": ["cron_expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_natural_language_to_cron",
            "description": "将自然语言描述转换为 Cron 表达式。只读操作。",
            "parameters": {
                "type": "object",
                "properties": {
                    "natural_text": {"type": "string", "description": "如'每天18:30'、'工作日09:00'"},
                },
                "required": ["natural_text"],
            },
        },
    },
]


def _get_all_tools_schema() -> list[dict]:
    """获取所有工具的 Function Calling Schema"""
    return BASE_TOOLS_SCHEMA + get_ops_tools_schema()


async def _execute_readonly_tool(tool_name: str, tool_args: dict, db: AsyncSession) -> str:
    """
    执行只读工具，返回结果字符串。
    只读工具可以直接调用，不需要用户确认。
    """
    # 无需 db 的基础工具
    if tool_name == "get_current_time":
        return get_current_time.invoke({})
    if tool_name == "calculate":
        return calculate.invoke(tool_args)
    if tool_name == "parse_cron_expression":
        return parse_cron_expression.invoke(tool_args)
    if tool_name == "convert_natural_language_to_cron":
        return convert_natural_language_to_cron.invoke(tool_args)

    # 需要 db 的运维查询工具
    ops_tools = make_ops_tools(db)
    ops_tool_map = {fn.__name__: fn for fn in ops_tools}

    if tool_name not in ops_tool_map:
        return f"未知工具：{tool_name}"

    tool_fn = ops_tool_map[tool_name]
    try:
        result = await tool_fn(**tool_args)
        return str(result)
    except Exception as e:
        return f"工具执行错误：{e}"


async def _execute_write_tool(tool_name: str, tool_args: dict, db: AsyncSession) -> str:
    """
    执行写操作工具（用户确认后调用此函数真正执行）。
    """
    ops_tools = make_ops_tools(db)
    ops_tool_map = {fn.__name__: fn for fn in ops_tools}

    if tool_name not in ops_tool_map:
        return f"未知工具：{tool_name}"

    tool_fn = ops_tool_map[tool_name]
    try:
        result = await tool_fn(**tool_args)
        return str(result)
    except Exception as e:
        return f"执行失败：{e}"


def _build_pending_description(tool_name: str, tool_args: dict) -> str:
    """
    根据工具名和参数生成人类可读的操作描述，用于前端确认框展示。
    """
    if tool_name == "execute_script_on_servers":
        server_ids = tool_args.get("server_ids", [])
        command = tool_args.get("command", "")
        env = tool_args.get("environment", "")
        env_str = f"（环境: {env}）" if env else ""
        return (
            f"在 **{len(server_ids)} 台**服务器{env_str}上执行命令：\n\n"
            f"```shell\n{command}\n```\n\n"
            f"目标服务器 ID：{server_ids}"
        )
    if tool_name == "create_scheduled_task":
        name = tool_args.get("name", "")
        cron = tool_args.get("cron_expression", "")
        command = tool_args.get("command", "")
        server_ids = tool_args.get("server_ids", [])
        desc = tool_args.get("description", "")
        try:
            from app.services.cron_helper import describe_cron_zh
            cron_desc = describe_cron_zh(cron)
        except Exception:
            cron_desc = cron
        return (
            f"创建定时任务：**{name}**\n\n"
            f"- 执行频率：`{cron}`（{cron_desc}）\n"
            f"- 执行命令：`{command}`\n"
            f"- 目标服务器：{len(server_ids)} 台（ID: {server_ids}）\n"
            + (f"- 备注：{desc}" if desc else "")
        )
    if tool_name == "toggle_task":
        task_id = tool_args.get("task_id", "")
        enable = tool_args.get("enable", True)
        action = "启用" if enable else "禁用"
        return f"将定时任务（ID: **{task_id}**）**{action}**"

    # 默认描述
    return f"执行操作：`{tool_name}`\n\n参数：```json\n{json.dumps(tool_args, ensure_ascii=False, indent=2)}\n```"


# ============ 核心对话逻辑 ============

async def ops_chat(
    db: AsyncSession,
    user_id: int,
    message: str,
    conversation_id: Optional[int] = None,
) -> dict:
    """
    运维 AI 对话（非流式）

    流程：
    1. 获取/创建对话
    2. 构建消息列表（含历史）
    3. 调用 LLM with Function Calling
    4. 如果 LLM 选择调用工具：
       - 只读工具 → 直接执行 → 将结果作为 tool 消息回传给 LLM → 获取最终回复
       - 写操作工具 → 不执行 → 返回 pending_action 给前端确认
    5. 保存消息到数据库

    Returns:
        {conversation_id, answer, pending_action, sources}
    """
    # 1. 获取或创建对话
    if conversation_id:
        conv = await conv_crud.get_conversation(db, conversation_id)
        if not conv:
            return {"error": "对话不存在"}
    else:
        title = message[:20] + "..." if len(message) > 20 else message
        conv = await conv_crud.create_conversation(db, user_id, kb_id=None, title=title)

    # 保存用户消息
    await conv_crud.add_message(db, conv.id, "user", message)

    # 2. 构建消息列表
    messages = [{"role": "system", "content": OPS_SYSTEM_PROMPT}]

    # 加入历史（最近 8 轮 = 16 条消息）
    if conv.messages:
        for msg in conv.messages[-16:]:
            messages.append({"role": msg.role, "content": msg.content})

    # 确保当前用户消息在最后
    if not messages or messages[-1].get("content") != message or messages[-1].get("role") != "user":
        messages.append({"role": "user", "content": message})

    # 3. 调用 LLM（携带工具列表）
    tools_schema = _get_all_tools_schema()
    sources = []
    pending_action = None
    answer = ""

    try:
        response = await call_llm(messages, stream=False, tools=tools_schema)
        choice = response.choices[0]
        msg = choice.message

        # 4. 处理工具调用
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]  # 每次处理第一个工具调用
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                tool_args = {}

            if tool_name in WRITE_OP_TOOL_NAMES:
                # 写操作：挂起，返回 pending_action 给前端确认
                description = _build_pending_description(tool_name, tool_args)
                pending_action = {
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "description": description,
                }
                answer = f"我需要执行一个操作，请确认后继续：\n\n{description}"
                sources.append("待用户确认")
            else:
                # 只读操作：直接执行，将结果回传给 LLM 获取最终回复
                sources.append(f"工具: {tool_name}")
                tool_result = await _execute_readonly_tool(tool_name, tool_args, db)

                # 将工具调用结果加入消息链，再次请求 LLM 生成自然语言回复
                messages.append({"role": "assistant", "content": None, "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ]})
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

                # 第二次调用 LLM，根据工具结果生成最终回复
                final_response = await call_llm(messages, stream=False)
                answer = final_response.choices[0].message.content or tool_result
        else:
            # 纯文字回复
            answer = msg.content or "抱歉，我暂时无法回答这个问题。"

    except ValueError as e:
        # AI 未配置
        answer = f"⚠️ AI 服务未配置：{e}"
    except Exception as e:
        logger.error(f"[OpsAgent] LLM 调用失败: {e}", exc_info=True)
        answer = f"抱歉，AI 服务暂时不可用：{str(e)}"

    # 5. 保存 AI 回复
    await conv_crud.add_message(db, conv.id, "assistant", answer, sources=sources)

    return {
        "conversation_id": conv.id,
        "answer": answer,
        "pending_action": pending_action,
        "sources": sources,
    }


async def ops_chat_stream(
    db: AsyncSession,
    user_id: int,
    message: str,
    conversation_id: Optional[int] = None,
) -> AsyncGenerator[str, None]:
    """
    运维 AI 对话（SSE 流式输出）

    流程与 ops_chat 相同，但 AI 回复通过 SSE 逐字符 yield。
    工具调用阶段不流式（工具执行完再流式输出最终回复）。

    SSE 格式：
        data: <text_chunk>\\n\\n        → 普通文本块
        data: [PENDING_ACTION]\\n\\n   → 写操作待确认（JSON）
        data: [TOOL_CALL] <name>\\n\\n → 工具调用通知
        data: [DONE]\\n\\n             → 结束
    """
    # 获取或创建对话
    if conversation_id:
        conv = await conv_crud.get_conversation(db, conversation_id)
        if not conv:
            yield "data: [ERROR] 对话不存在\n\n"
            return
    else:
        title = message[:20] + "..." if len(message) > 20 else message
        conv = await conv_crud.create_conversation(db, user_id, kb_id=None, title=title)

    await conv_crud.add_message(db, conv.id, "user", message)

    # 构建消息列表
    messages = [{"role": "system", "content": OPS_SYSTEM_PROMPT}]
    if conv.messages:
        for msg in conv.messages[-16:]:
            messages.append({"role": msg.role, "content": msg.content})
    if not messages or messages[-1].get("content") != message or messages[-1].get("role") != "user":
        messages.append({"role": "user", "content": message})

    tools_schema = _get_all_tools_schema()
    sources = []
    full_answer = ""

    try:
        # 第一次调用（非流式，检测是否有工具调用）
        response = await call_llm(messages, stream=False, tools=tools_schema)
        choice = response.choices[0]
        msg = choice.message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                tool_args = {}

            if tool_name in WRITE_OP_TOOL_NAMES:
                # 写操作：发送 PENDING_ACTION 事件
                description = _build_pending_description(tool_name, tool_args)
                pending_data = json.dumps({
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "description": description,
                    "conversation_id": conv.id,
                }, ensure_ascii=False)
                answer_text = f"我需要执行一个操作，请确认后继续：\n\n{description}"
                full_answer = answer_text
                # 先流式输出提示文字
                yield f"data: {answer_text}\n\n"
                yield f"data: [PENDING_ACTION]{pending_data}\n\n"
            else:
                # 只读工具：执行，通知前端，然后流式输出最终回复
                sources.append(f"工具: {tool_name}")
                yield f"data: [TOOL_CALL]{tool_name}\n\n"

                tool_result = await _execute_readonly_tool(tool_name, tool_args, db)

                messages.append({"role": "assistant", "content": None, "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ]})
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

                # 第二次调用（流式）
                stream_response = await call_llm(messages, stream=True)
                async for chunk in stream_response:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        full_answer += delta.content
                        yield f"data: {delta.content}\n\n"
        else:
            # 纯文字回复（流式）
            stream_response = await call_llm(messages, stream=True)
            async for chunk in stream_response:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_answer += delta.content
                    yield f"data: {delta.content}\n\n"

    except ValueError as e:
        err_msg = f"⚠️ AI 服务未配置：{e}"
        full_answer = err_msg
        yield f"data: {err_msg}\n\n"
    except Exception as e:
        logger.error(f"[OpsAgent] 流式调用失败: {e}", exc_info=True)
        err_msg = f"AI 服务暂时不可用：{str(e)}"
        full_answer = err_msg
        yield f"data: {err_msg}\n\n"
    finally:
        if full_answer:
            await conv_crud.add_message(db, conv.id, "assistant", full_answer, sources=sources)
        yield "data: [DONE]\n\n"


async def ops_confirm_action(
    db: AsyncSession,
    user_id: int,
    tool_name: str,
    tool_args: dict,
    conversation_id: int,
) -> dict:
    """
    用户确认写操作后执行

    Args:
        db: 数据库 session
        user_id: 当前用户 ID
        tool_name: 要执行的工具名
        tool_args: 工具参数
        conversation_id: 所属对话 ID

    Returns:
        {conversation_id, answer, success}
    """
    conv = await conv_crud.get_conversation(db, conversation_id)
    if not conv:
        return {"error": "对话不存在", "success": False}

    try:
        result = await _execute_write_tool(tool_name, tool_args, db)
        success = not result.startswith("❌") and "失败" not in result and "错误" not in result

        # 将执行结果加入对话
        answer = f"✅ 操作已执行：\n\n{result}"
        if not success:
            answer = f"❌ 操作执行失败：\n\n{result}"

        await conv_crud.add_message(db, conv.id, "assistant", answer, sources=["用户确认执行"])

        return {
            "conversation_id": conversation_id,
            "answer": answer,
            "success": success,
        }
    except Exception as e:
        logger.error(f"[OpsAgent] 确认执行失败: {e}", exc_info=True)
        error_msg = f"❌ 操作执行出错：{str(e)}"
        await conv_crud.add_message(db, conv.id, "assistant", error_msg)
        return {
            "conversation_id": conversation_id,
            "answer": error_msg,
            "success": False,
        }
