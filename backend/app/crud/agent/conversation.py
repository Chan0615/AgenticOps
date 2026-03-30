"""对话 CRUD"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.agent import Conversation, ConversationMessage


async def get_conversations(db: AsyncSession, user_id: int) -> List[Conversation]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
    )
    return result.scalars().all()


async def get_conversation(db: AsyncSession, conv_id: int) -> Optional[Conversation]:
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == conv_id)
    )
    return result.scalar_one_or_none()


async def create_conversation(
    db: AsyncSession, user_id: int, kb_id: int = None, title: str = "新对话"
) -> Conversation:
    conv = Conversation(user_id=user_id, kb_id=kb_id, title=title)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


async def delete_conversation(db: AsyncSession, conv_id: int) -> bool:
    conv = await get_conversation(db, conv_id)
    if not conv:
        return False
    await db.delete(conv)
    await db.commit()
    return True


async def add_message(
    db: AsyncSession,
    conversation_id: int,
    role: str,
    content: str,
    sources: list = None,
    tool_calls: list = None,
) -> ConversationMessage:
    msg = ConversationMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
        sources=sources,
        tool_calls=tool_calls,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def update_conversation_title(db: AsyncSession, conv_id: int, title: str):
    conv = await get_conversation(db, conv_id)
    if conv:
        conv.title = title[:255]
        await db.commit()
