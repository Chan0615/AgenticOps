"""
Tools 工具集 - 支持时间、天气等外部信息查询
"""

import os
import requests
from datetime import datetime
from typing import Optional
from langchain_core.tools import tool


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


# 工具注册表
TOOLS = [
    get_current_time,
    calculate,
]


def get_tools():
    """获取所有可用工具"""
    return TOOLS


def execute_tool(tool_name: str, **kwargs) -> str:
    """
    执行指定工具
    
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
