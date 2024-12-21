# backend/chat/dao.py
from sqlalchemy import select

from backend.dao.base import BaseDAO
from backend.chat.models import ChatMessage
from backend.database import async_session_maker


class ChatDAO(BaseDAO):
    model = ChatMessage

    @classmethod
    async def create_message(cls, sender_id: int, receiver_id: int, message: str):
        async with async_session_maker() as session:
            new_message = cls.model(sender_id=sender_id, receiver_id=receiver_id, message=message)
            session.add(new_message)
            await session.commit()
            await session.refresh(new_message)
            return new_message

    @classmethod
    async def get_messages(cls, user_id: int, other_user_id: int):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(
                ((cls.model.sender_id == user_id) & (cls.model.receiver_id == other_user_id)) |
                ((cls.model.sender_id == other_user_id) & (cls.model.receiver_id == user_id))
            ).order_by(cls.model.timestamp)
            result = await session.execute(stmt)
            return result.scalars().all()