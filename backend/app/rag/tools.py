"""
Tools 工具集 - 支持时间查询、数学计算、运维操作

工具分为两类：
  - 只读工具：AI 可直接调用，查询服务器/脚本/任务/日志等信息
  - 写操作工具：标记 is_write_op=True，需用户在前端确认后由 confirm 接口触发
"""

import os
import json
from datetime import datetime
from typing import Optional


def _get_tool_decorator():
    """懒加载 langchain_core.tools.tool 装饰器"""
    try:
        from langchain_core.tools import tool
        return tool
    except ImportError:
        # 如果没有安装 langchain_core，返回一个 no-op 装饰器
        # 工具函数仍然可以直接调用，只是没有 LangChain Tool 接口
        def noop_tool(func):
            func.name = func.__name__
            func.invoke = lambda kwargs: func(**kwargs)
            return func
        return noop_tool


# 使用懒加载装饰器
tool = _get_tool_decorator()


# ============ 通用工具（无需 db session）============

@tool
def get_current_time() -> str:
    """
    获取当前系统时间，包括日期、时间和星期几。

    当用户询问当前时间、今天日期、星期几等问题时使用此工具。
    """
    now = datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

    time_str = now.strftime('%H:%M:%S')
    date_str = now.strftime('%Y年%m月%d日')
    weekday = weekdays[now.weekday()]

    return f"当前时间：{time_str}\n日期：{date_str}\n{weekday}"


@tool
def calculate(expression: str) -> str:
    """
    计算数学表达式。

    Args:
        expression: 数学表达式，如 "1 + 2 * 3"、"sqrt(16)"、"2 ** 10"

    当用户需要进行数学计算时使用此工具。
    """
    try:
        # 安全评估：只允许基本数学运算
        allowed_names = {
            "abs": abs,
            "max": max,
            "min": min,
            "pow": pow,
            "round": round,
            "sum": sum,
        }

        # 清理表达式，移除潜在危险字符
        cleaned = expression.replace("__", "").replace("import", "").replace("exec", "").replace("eval", "")

        result = eval(cleaned, {"__builtins__": {}}, allowed_names)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"


@tool
def parse_cron_expression(cron_expression: str) -> str:
    """
    解释 Cron 表达式的含义，将其转换为人类可读的中文描述。

    Args:
        cron_expression: 标准 5 段 Cron 表达式，如 "0 9 * * 1-5"

    用于帮助用户理解定时任务的执行频率。
    """
    try:
        from app.services.cron_helper import describe_cron_zh, validate_cron
        valid, error = validate_cron(cron_expression)
        if not valid:
            return f"无效的 Cron 表达式：{error}"
        description = describe_cron_zh(cron_expression)
        return f"Cron 表达式 `{cron_expression}` 的含义：{description}"
    except Exception as e:
        return f"解析失败：{e}"


@tool
def convert_natural_language_to_cron(natural_text: str) -> str:
    """
    将自然语言描述转换为 Cron 表达式。

    Args:
        natural_text: 自然语言描述，如"每天18:30"、"工作日09:00"、"每周一,三,五20:00"、"每月5号18:30"

    用于帮助用户创建定时任务时生成 Cron 表达式。
    """
    try:
        from app.services.cron_helper import natural_to_cron, describe_cron_zh
        cron = natural_to_cron(natural_text)
        description = describe_cron_zh(cron)
        return f"转换成功！Cron 表达式：`{cron}`\n含义：{description}"
    except ValueError as e:
        return f"转换失败：{e}"
    except Exception as e:
        return f"转换错误：{e}"


# ============ 基础工具注册表（无需 db 的工具）============
TOOLS = [
    get_current_time,
    calculate,
    parse_cron_expression,
    convert_natural_language_to_cron,
]


def get_tools():
    """获取所有基础工具（不含需要 db 的运维工具）"""
    return TOOLS


def execute_tool(tool_name: str, **kwargs) -> str:
    """
    执行基础工具（同步接口，用于 agents.py 中的 RAG 工具调用）

    Args:
        tool_name: 工具名称
        **kwargs: 工具参数

    Returns:
        工具执行结果
    """
    tool_map = {t.name: t for t in TOOLS}

    if tool_name not in tool_map:
        return f"未知工具：{tool_name}"

    try:
        tool_func = tool_map[tool_name]
        result = tool_func.invoke(kwargs)
        return str(result)
    except Exception as e:
        return f"工具执行错误：{e}"


# ============ 运维工具（需要 db session，使用工厂函数模式）============

# 标记写操作工具名称，AI 调用这些工具时需要用户确认
WRITE_OP_TOOL_NAMES = {
    "execute_script_on_servers",
    "create_scheduled_task",
    "toggle_task",
}


def make_ops_tools(db) -> list:
    """
    工厂函数：创建需要 db session 的运维工具列表。

    使用闭包将 db session 注入到工具函数中，遵循 LangChain @tool 模式。

    Args:
        db: AsyncSession 实例

    Returns:
        工具函数列表（供 Function Calling 使用）
    """

    # ---- 只读工具 ----

    async def query_servers(
        name: str = None,
        environment: str = None,
        status: str = None,
        limit: int = 20,
    ) -> str:
        """
        查询服务器列表。

        Args:
            name: 按名称模糊搜索（可选）
            environment: 按环境过滤，如 production / staging / testing（可选）
            status: 按状态过滤，如 online / offline（可选）
            limit: 返回数量上限，默认 20

        返回服务器列表信息，包括 ID、名称、主机名、环境、状态等。
        """
        try:
            from app.crud.ops import server as server_crud
            servers, total = await server_crud.get_servers(
                db,
                skip=0,
                limit=min(limit, 50),
                name=name,
                environment=environment,
                status=status,
            )
            if not servers:
                return "未找到符合条件的服务器。"

            lines = [f"共找到 {total} 台服务器（显示前 {len(servers)} 台）：\n"]
            for s in servers:
                lines.append(
                    f"- ID:{s.id} | {s.name} | {s.hostname} | 环境:{s.environment or '未设置'} | 状态:{s.status or '未知'}"
                )
            return "\n".join(lines)
        except Exception as e:
            return f"查询服务器失败：{e}"

    async def query_scripts(
        name: str = None,
        script_type: str = None,
        limit: int = 20,
    ) -> str:
        """
        查询脚本列表。

        Args:
            name: 按名称模糊搜索（可选）
            script_type: 脚本类型，如 shell / python（可选）
            limit: 返回数量上限，默认 20

        返回脚本列表信息，包括 ID、名称、类型、所属项目/分组等。
        """
        try:
            from app.crud.ops import script as script_crud
            scripts, total = await script_crud.get_scripts(
                db,
                skip=0,
                limit=min(limit, 50),
                name=name,
                script_type=script_type,
            )
            if not scripts:
                return "未找到符合条件的脚本。"

            lines = [f"共找到 {total} 个脚本（显示前 {len(scripts)} 个）：\n"]
            for s in scripts:
                project_name = s.project.name if s.project else "未分类"
                group_name = s.group.name if s.group else "-"
                lines.append(
                    f"- ID:{s.id} | {s.name} | 类型:{s.script_type} | 项目:{project_name} | 分组:{group_name}"
                )
            return "\n".join(lines)
        except Exception as e:
            return f"查询脚本失败：{e}"

    async def query_tasks(
        name: str = None,
        enabled: bool = None,
        limit: int = 20,
    ) -> str:
        """
        查询定时任务列表。

        Args:
            name: 按任务名称模糊搜索（可选）
            enabled: 是否只显示启用中的任务，True=启用，False=禁用，不填=全部（可选）
            limit: 返回数量上限，默认 20

        返回定时任务信息，包括 ID、名称、Cron 表达式、启用状态、下次执行时间等。
        """
        try:
            from app.crud.ops import task as task_crud
            from app.services.cron_helper import describe_cron_zh
            tasks, total = await task_crud.get_tasks(
                db,
                skip=0,
                limit=min(limit, 50),
                name=name,
                enabled=enabled,
            )
            if not tasks:
                return "未找到符合条件的定时任务。"

            lines = [f"共找到 {total} 个定时任务（显示前 {len(tasks)} 个）：\n"]
            for t in tasks:
                try:
                    cron_desc = describe_cron_zh(t.cron_expression)
                except Exception:
                    cron_desc = t.cron_expression
                enabled_str = "✅ 启用" if t.enabled else "❌ 禁用"
                next_run = t.next_run_at.strftime("%Y-%m-%d %H:%M:%S") if t.next_run_at else "未知"
                lines.append(
                    f"- ID:{t.id} | {t.name} | {enabled_str} | {t.cron_expression}（{cron_desc}）| 下次执行:{next_run}"
                )
            return "\n".join(lines)
        except Exception as e:
            return f"查询定时任务失败：{e}"

    async def query_execution_logs(
        task_name: str = None,
        server_keyword: str = None,
        status: str = None,
        limit: int = 10,
    ) -> str:
        """
        查询任务执行日志。

        Args:
            task_name: 按任务名称模糊搜索（可选）
            server_keyword: 按服务器名/主机名模糊搜索（可选）
            status: 按执行状态过滤：pending / running / success / failed（可选）
            limit: 返回数量上限，默认 10

        返回最近的执行日志，包括任务名、服务器、状态、执行时间等。
        """
        try:
            from app.crud.ops import log as log_crud
            logs, total = await log_crud.get_execution_logs(
                db,
                skip=0,
                limit=min(limit, 30),
                task_name=task_name,
                server_keyword=server_keyword,
                status=status,
            )
            if not logs:
                return "未找到符合条件的执行日志。"

            lines = [f"共找到 {total} 条执行记录（显示最近 {len(logs)} 条）：\n"]
            for log in logs:
                task_name_str = log.task.name if log.task else "未知任务"
                server_str = f"{log.server.name}({log.server.hostname})" if log.server else "未知服务器"
                status_emoji = {"success": "✅", "failed": "❌", "running": "🔄", "pending": "⏳"}.get(log.status, "❓")
                created = log.created_at.strftime("%m-%d %H:%M") if log.created_at else "-"
                duration = f"{log.duration:.1f}s" if log.duration else "-"
                lines.append(
                    f"- {status_emoji} [{created}] {task_name_str} @ {server_str} | 耗时:{duration} | 退出码:{log.exit_code}"
                )
            return "\n".join(lines)
        except Exception as e:
            return f"查询执行日志失败：{e}"

    # ---- 写操作工具（标记后由前端确认再执行）----

    async def execute_script_on_servers(
        server_ids: list,
        command: str,
        environment: str = None,
    ) -> str:
        """
        [写操作] 在指定服务器上执行 Shell 命令或脚本。

        Args:
            server_ids: 目标服务器 ID 列表，如 [1, 2, 3]
            command: 要执行的 Shell 命令或脚本路径
            environment: 运行环境名称（可选，不填则根据服务器的 environment 字段自动选择）

        ⚠️ 此操作将在真实服务器上执行命令，请谨慎确认。
        """
        try:
            from app.crud.ops import server as server_crud
            from app.services.salt_service import salt_service

            results = []
            for server_id in server_ids:
                server = await server_crud.get_server(db, server_id)
                if not server:
                    results.append(f"服务器 ID:{server_id} 不存在")
                    continue
                env_name = environment or server.environment
                target = server.salt_minion_id or server.hostname
                try:
                    result = await salt_service.run_shell_command(
                        env_name=env_name,
                        target=target,
                        command=command,
                    )
                    returns = result.get("return", [{}])[0] if result else {}
                    output = returns.get(target, "无输出")
                    results.append(f"✅ {server.name}({target}): {str(output)[:200]}")
                except Exception as e:
                    results.append(f"❌ {server.name}({target}): 执行失败 - {e}")

            return "\n".join(results)
        except Exception as e:
            return f"执行失败：{e}"

    async def create_scheduled_task(
        name: str,
        cron_expression: str,
        command: str,
        server_ids: list,
        description: str = None,
    ) -> str:
        """
        [写操作] 创建一个新的定时任务。

        Args:
            name: 任务名称
            cron_expression: Cron 表达式，如 "0 9 * * 1-5"
            command: 要执行的命令
            server_ids: 目标服务器 ID 列表
            description: 任务描述（可选）

        ⚠️ 此操作将创建并保存新的定时任务。
        """
        try:
            from app.crud.ops import task as task_crud
            from app.schemas.task import ScheduledTaskCreate
            from app.services.cron_helper import validate_cron, describe_cron_zh

            # 验证 cron 表达式
            valid, error = validate_cron(cron_expression)
            if not valid:
                return f"Cron 表达式无效：{error}"

            task_data = ScheduledTaskCreate(
                name=name,
                cron_expression=cron_expression,
                command=command,
                server_ids=server_ids,
                description=description or "",
                task_type="salt",
                enabled=True,
            )
            task = await task_crud.create_task(db, task_data, created_by="ai-agent")
            cron_desc = describe_cron_zh(cron_expression)
            return (
                f"✅ 定时任务创建成功！\n"
                f"- ID: {task.id}\n"
                f"- 名称: {task.name}\n"
                f"- 执行频率: {cron_expression}（{cron_desc}）\n"
                f"- 目标服务器: {len(server_ids)} 台\n"
                f"- 状态: 已启用"
            )
        except Exception as e:
            return f"创建任务失败：{e}"

    async def toggle_task(task_id: int, enable: bool) -> str:
        """
        [写操作] 启用或禁用一个定时任务。

        Args:
            task_id: 定时任务 ID
            enable: True 表示启用，False 表示禁用

        ⚠️ 此操作将改变定时任务的调度状态。
        """
        try:
            from app.crud.ops import task as task_crud
            task = await task_crud.get_task(db, task_id)
            if not task:
                return f"定时任务 ID:{task_id} 不存在"

            if task.enabled == enable:
                status_str = "已启用" if enable else "已禁用"
                return f"任务「{task.name}」当前状态已经是{status_str}，无需操作。"

            updated = await task_crud.toggle_task_enabled(db, task_id, updated_by="ai-agent")
            action = "启用" if enable else "禁用"
            return f"✅ 已成功{action}定时任务「{updated.name}」（ID:{task_id}）"
        except Exception as e:
            return f"操作失败：{e}"

    # 返回所有运维工具（包含只读和写操作）
    return [
        query_servers,
        query_scripts,
        query_tasks,
        query_execution_logs,
        execute_script_on_servers,
        create_scheduled_task,
        toggle_task,
    ]


def get_ops_tools_schema() -> list[dict]:
    """
    返回运维工具的 OpenAI Function Calling Schema 列表。
    用于在调用 LLM 时传入 tools 参数。
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "query_servers",
                "description": "查询服务器列表，支持按名称、环境、状态过滤。只读操作。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "服务器名称（模糊匹配）"},
                        "environment": {"type": "string", "description": "运行环境，如 production/staging/testing"},
                        "status": {"type": "string", "description": "服务器状态，如 online/offline"},
                        "limit": {"type": "integer", "description": "返回数量上限，默认20", "default": 20},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "query_scripts",
                "description": "查询脚本列表，支持按名称、类型过滤。只读操作。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "脚本名称（模糊匹配）"},
                        "script_type": {"type": "string", "description": "脚本类型，如 shell/python"},
                        "limit": {"type": "integer", "description": "返回数量上限，默认20", "default": 20},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "query_tasks",
                "description": "查询定时任务列表，支持按名称、启用状态过滤。只读操作。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "任务名称（模糊匹配）"},
                        "enabled": {"type": "boolean", "description": "是否启用，true=启用，false=禁用"},
                        "limit": {"type": "integer", "description": "返回数量上限，默认20", "default": 20},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "query_execution_logs",
                "description": "查询任务执行日志，支持按任务名、服务器、状态过滤。只读操作。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_name": {"type": "string", "description": "任务名称（模糊匹配）"},
                        "server_keyword": {"type": "string", "description": "服务器名称或主机名（模糊匹配）"},
                        "status": {"type": "string", "description": "执行状态：pending/running/success/failed"},
                        "limit": {"type": "integer", "description": "返回数量上限，默认10", "default": 10},
                    },
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
                        "cron_expression": {"type": "string", "description": "标准5段Cron表达式，如 '0 9 * * 1-5'"},
                    },
                    "required": ["cron_expression"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "convert_natural_language_to_cron",
                "description": "将自然语言转换为 Cron 表达式。只读操作。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "natural_text": {"type": "string", "description": "如'每天18:30'、'工作日09:00'、'每周一,三,五20:00'"},
                    },
                    "required": ["natural_text"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "execute_script_on_servers",
                "description": "⚠️[写操作-需确认] 在指定服务器上执行 Shell 命令或脚本。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "server_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "目标服务器 ID 列表",
                        },
                        "command": {"type": "string", "description": "要执行的 Shell 命令或脚本路径"},
                        "environment": {"type": "string", "description": "运行环境名称（可选）"},
                    },
                    "required": ["server_ids", "command"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_scheduled_task",
                "description": "⚠️[写操作-需确认] 创建新的定时任务。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "任务名称"},
                        "cron_expression": {"type": "string", "description": "Cron表达式"},
                        "command": {"type": "string", "description": "要执行的命令"},
                        "server_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "目标服务器 ID 列表",
                        },
                        "description": {"type": "string", "description": "任务描述（可选）"},
                    },
                    "required": ["name", "cron_expression", "command", "server_ids"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "toggle_task",
                "description": "⚠️[写操作-需确认] 启用或禁用定时任务。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "定时任务 ID"},
                        "enable": {"type": "boolean", "description": "true=启用，false=禁用"},
                    },
                    "required": ["task_id", "enable"],
                },
            },
        },
    ]
