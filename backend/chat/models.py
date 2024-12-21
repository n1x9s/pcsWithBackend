# backend/chat/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("Users", foreign_keys=[Column("sender_id", Integer, ForeignKey("users.id"))])
    receiver = relationship("Users", foreign_keys=[Column("receiver_id", Integer, ForeignKey("users.id"))])