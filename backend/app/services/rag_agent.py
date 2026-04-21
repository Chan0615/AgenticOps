"""
Agent RAG 核心服务

参照 astordu/rag_agent 的 Agentic RAG 思路：
- Agent 自主决定何时检索
- Agent 可以多次检索（不同查询）
- Agent 自动改写查询以获得更好结果
- 检索结果作为工具返回给 Agent
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List, Optional
from app.crud.agent import document as doc_crud
from app.crud.agent import conversation as conv_crud
from app.core import config
import logging

logger = logging.getLogger(__name__)


# ============ AI 模型调用 ============
def _get_ai_config() -> dict:
    """获取 AI 配置（优先 qwen）"""
    for provider in ["qwen", "deepseek", "openai"]:
        try:
            cfg = config.get_ai_config(provider)
            if cfg.get("enabled") and cfg.get("api_key"):
                return cfg
        except KeyError:
            continue
    return {}


async def call_llm(messages: list[dict], stream: bool = False):
    """
    调用 LLM（OpenAI 兼容接口）
    适配阿里云 DashScope / DeepSeek / OpenAI
    """
    from openai import AsyncOpenAI

    cfg = _get_ai_config()
    if not cfg:
        raise ValueError("未配置 AI 模型，请在 config.yaml 中设置 api_key")

    client = AsyncOpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"],
    )

    response = await client.chat.completions.create(
        model=cfg["model"],
        messages=messages,
        stream=stream,
        temperature=0.7,
        max_tokens=4096,
    )
    return response


# ============ 检索工具 ============
async def retriever_tool(
    db: AsyncSession, kb_id: int, query: str, top_k: int = 5
) -> str:
    """
    检索工具 - Agent 可多次调用
    后续替换为向量搜索（FAISS / Milvus）
    """
    logger.info(f"[RAG] 检索: kb={kb_id}, query={query}")
    chunks = await doc_crud.search_chunks(db, kb_id, query, top_k)
    if not chunks:
        return "未找到相关资料。"

    results = []
    for i, chunk in enumerate(chunks):
        results.append(f"资料{i + 1}: {chunk.content}")
    return "\n\n".join(results)


# ============ Agent Prompt ============
AGENT_SYSTEM_PROMPT = """你是「托马斯回旋喵」，一个基于知识库的智能问答助手。

你有 retriever 工具可以搜索知识库。回答规则：
1. 先理解用户问题，用肯定句形式搜索（如"FastAPI 最佳实践"而非"FastAPI 怎么用"）
2. 如果第一次搜索结果不够好，尝试用不同关键词再次搜索
3. 综合多次搜索结果给出完整回答
4. 如果确实找不到相关资料，诚实告知
5. 回答简洁有条理，必要时引用来源"""

RAG_CONTEXT_PROMPT = """以下是知识库中检索到的相关资料：

---
{context}
---

请基于以上资料回答用户问题。如果资料不足请说明。"""


# ============ 对话 ============
async def chat(
    db: AsyncSession,
    user_id: int,
    message: str,
    kb_id: int = None,
    conversation_id: int = None,
) -> dict:
    """普通对话"""
    # 获取或创建对话
    if conversation_id:
        conv = await conv_crud.get_conversation(db, conversation_id)
    else:
        title = message[:20] + "..." if len(message) > 20 else message
        conv = await conv_crud.create_conversation(
            db, user_id, kb_id=kb_id, title=title
        )

    if not conv:
        return {"error": "对话不存在"}

    # 保存用户消息
    await conv_crud.add_message(db, conv.id, "user", message)

    # 检索资料
    sources = []
    context = ""
    if kb_id:
        # 第一次检索：用问题本身
        chunk1 = await retriever_tool(db, kb_id, message)
        context = chunk1
        sources.append("语义检索")

        # Agent 策略：结果不足时用关键词再搜
        if "未找到" in context or len(context) < 100:
            keywords = _extract_keywords(message)
            if keywords and keywords != message:
                chunk2 = await retriever_tool(db, kb_id, keywords)
                if "未找到" not in chunk2:
                    context += "\n\n" + chunk2
                    sources.append("关键词扩展检索")

    # 构造消息
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]

    # 加入历史（最近 5 轮）
    # 仅对已有对话加载历史；新建对话 messages 未 eager-load，直接跳过
    if conversation_id and conv.messages:
        for msg in conv.messages[-10:]:
            messages.append({"role": msg.role, "content": msg.content})

    # 当前问题（带上下文）
    if context and "未找到" not in context:
        user_content = (
            RAG_CONTEXT_PROMPT.format(context=context) + f"\n\n用户问题：{message}"
        )
    else:
        user_content = message
    messages.append({"role": "user", "content": user_content})

    # 调用 LLM
    try:
        response = await call_llm(messages, stream=False)
        answer = response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        answer = f"抱歉，AI 模型调用失败：{str(e)}\n\n请检查 config.yaml 中的 AI 配置（api_key 是否正确）。"

    # 保存 AI 回复
    await conv_crud.add_message(db, conv.id, "assistant", answer, sources=sources)

    return {
        "conversation_id": conv.id,
        "answer": answer,
        "sources": sources,
    }


async def chat_stream(
    db: AsyncSession,
    user_id: int,
    message: str,
    kb_id: int = None,
    conversation_id: int = None,
) -> AsyncGenerator[str, None]:
    """流式对话（SSE）"""
    # 获取或创建对话
    if conversation_id:
        conv = await conv_crud.get_conversation(db, conversation_id)
    else:
        title = message[:20] + "..." if len(message) > 20 else message
        conv = await conv_crud.create_conversation(
            db, user_id, kb_id=kb_id, title=title
        )

    if not conv:
        yield "错误：对话不存在"
        return

    await conv_crud.add_message(db, conv.id, "user", message)

    # 检索
    context = ""
    sources = []
    if kb_id:
        context = await retriever_tool(db, kb_id, message)
        sources.append("知识库检索")

    # 构造消息
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    if context and "未找到" not in context:
        user_content = (
            RAG_CONTEXT_PROMPT.format(context=context) + f"\n\n用户问题：{message}"
        )
    else:
        user_content = message
    messages.append({"role": "user", "content": user_content})

    # 流式调用
    full_answer = ""
    try:
        response = await call_llm(messages, stream=True)
        async for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                full_answer += delta.content
                yield delta.content
    except Exception as e:
        yield f"错误：{str(e)}"

    # 保存完整回复
    if full_answer:
        await conv_crud.add_message(
            db, conv.id, "assistant", full_answer, sources=sources
        )


def _extract_keywords(question: str) -> str:
    """简单关键词提取"""
    stops = {
        "什么",
        "怎么",
        "如何",
        "为什么",
        "吗",
        "呢",
        "？",
        "?",
        "的",
        "了",
        "是",
        "有",
        "请",
        "帮",
        "我",
    }
    return "".join(w for w in question if w not in stops)
