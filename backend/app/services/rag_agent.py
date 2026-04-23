"""
RAG 知识库对话服务

基于混合检索（向量 + BM25）的对话服务：
- 对话记忆：加载历史对话上下文
- 智能检索：根据用户问题进行双重召回
- SSE 流式输出：实时返回 AI 回复
"""

import json
import logging
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ai import call_llm
from app.crud.agent import conversation as conv_crud
from app.services.hybrid_retriever import hybrid_search, format_context
from app.services.vector_store import generate_embedding

logger = logging.getLogger(__name__)


# ============ System Prompt ============

RAG_SYSTEM_PROMPT = """你是一个基于知识库的智能问答助手。

你的工作方式：
1. 根据提供的知识库资料来回答用户问题
2. 优先引用资料中的信息，确保回答准确
3. 如果资料不足以回答问题，诚实告知并说明需要哪些信息
4. 回答简洁有条理，使用 Markdown 格式
5. 当引用资料时，标注来源编号（如 [资料1]）
6. 结合对话历史理解用户的追问和上下文"""

RAG_CONTEXT_TEMPLATE = """以下是从知识库中检索到的相关资料：

{context}

---

请基于以上资料回答用户问题。如果资料不足以完整回答，请说明。"""

NO_CONTEXT_HINT = "知识库中未找到与此问题直接相关的资料。我将根据已有知识尝试回答。"


# ============ 核心对话 ============


async def chat(
    db: AsyncSession,
    user_id: int,
    message: str,
    kb_id: Optional[int] = None,
    conversation_id: Optional[int] = None,
) -> dict:
    """
    RAG 知识库对话（非流式）

    Returns:
        {
            "conversation_id": int,
            "answer": str,
            "sources": [str],
            "retrieved_chunks": int,
        }
    """
    # 1. 获取或创建对话
    if conversation_id:
        conv = await conv_crud.get_conversation(db, conversation_id)
        if not conv:
            return {"error": "对话不存在"}
    else:
        title = message[:20] + "..." if len(message) > 20 else message
        conv = await conv_crud.create_conversation(
            db, user_id, kb_id=kb_id, title=title
        )

    # 保存用户消息
    await conv_crud.add_message(db, conv.id, "user", message)

    # 2. 检索知识库
    sources = []
    context = ""
    retrieved_count = 0

    if kb_id:
        try:
            query_embedding = await generate_embedding(message)
            results = await hybrid_search(
                kb_id=kb_id,
                query=message,
                query_embedding=query_embedding,
                top_k=5,
            )
            if results:
                context = format_context(results)
                retrieved_count = len(results)
                # 收集来源信息
                seen_sources = set()
                for r in results:
                    src = r.get("metadata", {}).get("source", "")
                    rtype = r.get("retrieval_type", "")
                    if src and src not in seen_sources:
                        sources.append(f"{src}")
                        seen_sources.add(src)
                    if rtype == "hybrid":
                        if "混合检索" not in sources:
                            sources.append("混合检索")
                    elif rtype == "vector":
                        if "语义检索" not in sources:
                            sources.append("语义检索")
                    elif rtype == "bm25":
                        if "关键词检索" not in sources:
                            sources.append("关键词检索")
        except Exception as e:
            logger.error(f"[RAG] 检索失败: {e}", exc_info=True)
            sources.append("检索异常")

    # 3. 构建 LLM 消息
    messages = [{"role": "system", "content": RAG_SYSTEM_PROMPT}]

    # 加入对话历史（最近 16 条消息）
    if conversation_id and conv.messages:
        for msg in conv.messages[-16:]:
            messages.append({"role": msg.role, "content": msg.content})

    # 当前问题（带检索上下文）
    if context:
        user_content = RAG_CONTEXT_TEMPLATE.format(context=context) + f"\n\n用户问题：{message}"
    else:
        if kb_id:
            user_content = f"{NO_CONTEXT_HINT}\n\n用户问题：{message}"
        else:
            user_content = message

    # 避免重复添加（历史中可能已有）
    if not messages or messages[-1].get("content") != message:
        messages.append({"role": "user", "content": user_content})

    # 4. 调用 LLM
    try:
        response = await call_llm(messages, stream=False)
        answer = response.choices[0].message.content or "抱歉，我暂时无法回答这个问题。"
    except ValueError as e:
        answer = f"AI 服务未配置：{e}"
    except Exception as e:
        logger.error(f"[RAG] LLM 调用失败: {e}", exc_info=True)
        answer = f"AI 服务暂时不可用：{str(e)}"

    # 5. 保存回复
    await conv_crud.add_message(db, conv.id, "assistant", answer, sources=sources)

    return {
        "conversation_id": conv.id,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_count,
    }


async def chat_stream(
    db: AsyncSession,
    user_id: int,
    message: str,
    kb_id: Optional[int] = None,
    conversation_id: Optional[int] = None,
) -> AsyncGenerator[str, None]:
    """
    RAG 知识库对话（SSE 流式）

    SSE 事件：
    - data: [RETRIEVING]           — 正在检索
    - data: [CONTEXT]{json}        — 检索结果摘要
    - data: 普通文本               — AI 回复流式输出
    - data: [DONE]{json}           — 完成
    - data: [ERROR]msg             — 错误
    """

    def _sse(text: str) -> str:
        return "data: " + text.replace("\n", "\\n") + "\n\n"

    # 1. 获取或创建对话
    if conversation_id:
        conv = await conv_crud.get_conversation(db, conversation_id)
        if not conv:
            yield "data: [ERROR]对话不存在\n\n"
            return
    else:
        title = message[:20] + "..." if len(message) > 20 else message
        conv = await conv_crud.create_conversation(
            db, user_id, kb_id=kb_id, title=title
        )

    await conv_crud.add_message(db, conv.id, "user", message)

    # 2. 检索知识库
    sources = []
    context = ""
    retrieved_count = 0

    if kb_id:
        yield "data: [RETRIEVING]\n\n"
        try:
            query_embedding = await generate_embedding(message)
            results = await hybrid_search(
                kb_id=kb_id,
                query=message,
                query_embedding=query_embedding,
                top_k=5,
            )
            if results:
                context = format_context(results)
                retrieved_count = len(results)
                seen_sources = set()
                for r in results:
                    src = r.get("metadata", {}).get("source", "")
                    if src and src not in seen_sources:
                        sources.append(src)
                        seen_sources.add(src)

                # 发送检索摘要
                context_info = json.dumps(
                    {"count": retrieved_count, "sources": sources},
                    ensure_ascii=False,
                )
                yield f"data: [CONTEXT]{context_info}\n\n"
        except Exception as e:
            logger.error(f"[RAG] 检索失败: {e}", exc_info=True)

    # 3. 构建消息
    messages = [{"role": "system", "content": RAG_SYSTEM_PROMPT}]

    # 对话历史
    if conversation_id and conv.messages:
        for msg in conv.messages[-16:]:
            messages.append({"role": msg.role, "content": msg.content})

    if context:
        user_content = RAG_CONTEXT_TEMPLATE.format(context=context) + f"\n\n用户问题：{message}"
    else:
        if kb_id:
            user_content = f"{NO_CONTEXT_HINT}\n\n用户问题：{message}"
        else:
            user_content = message

    if not messages or messages[-1].get("content") != message:
        messages.append({"role": "user", "content": user_content})

    # 4. 流式调用 LLM
    full_answer = ""
    try:
        stream_response = await call_llm(messages, stream=True)
        async for chunk in stream_response:
            delta = chunk.choices[0].delta
            if delta.content:
                full_answer += delta.content
                yield _sse(delta.content)
    except ValueError as e:
        err = f"AI 服务未配置：{e}"
        full_answer = err
        yield _sse(err)
    except Exception as e:
        logger.error(f"[RAG] 流式调用失败: {e}", exc_info=True)
        err = f"AI 服务暂时不可用：{str(e)}"
        full_answer = err
        yield _sse(err)

    # 5. 保存完整回复
    if full_answer:
        await conv_crud.add_message(
            db, conv.id, "assistant", full_answer, sources=sources
        )

    # 6. 完成
    done_data = json.dumps(
        {
            "conversation_id": conv.id,
            "sources": sources,
            "retrieved_chunks": retrieved_count,
        },
        ensure_ascii=False,
    )
    yield f"data: [DONE]{done_data}\n\n"
