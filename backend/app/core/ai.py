"""
公共 AI 调用层

统一管理 LLM 配置读取与调用，消除 rag_agent.py / agents.py 中的代码重复。
"""

from app.core import config
import logging

logger = logging.getLogger(__name__)


def get_ai_config() -> dict:
    """
    获取 AI 配置，按优先级探测：qwen → deepseek → openai
    返回第一个 enabled=True 且有 api_key 的 provider 配置。
    """
    for provider in ["qwen", "deepseek", "openai"]:
        try:
            cfg = config.get_ai_config(provider)
            if cfg.get("enabled") and cfg.get("api_key"):
                return cfg
        except KeyError:
            continue
    return {}


async def call_llm(messages: list[dict], stream: bool = False, tools: list = None):
    """
    调用 LLM（OpenAI 兼容接口）

    支持：阿里云 DashScope / DeepSeek / OpenAI
    支持 Function Calling（传入 tools 参数）
    支持流式输出（stream=True）

    Args:
        messages: 消息列表，格式为 [{"role": "...", "content": "..."}]
        stream: 是否流式输出
        tools: OpenAI Function Calling 工具列表（可选）

    Returns:
        ChatCompletion 或 AsyncStream
    """
    from openai import AsyncOpenAI

    cfg = get_ai_config()
    if not cfg:
        raise ValueError("未配置 AI 模型，请在 config.yaml 中设置 ai.xxx.api_key 和 enabled: true")

    client = AsyncOpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"],
    )

    kwargs = dict(
        model=cfg["model"],
        messages=messages,
        stream=stream,
        temperature=0.7,
        max_tokens=4096,
    )
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    response = await client.chat.completions.create(**kwargs)
    return response
