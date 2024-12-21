# backend/chat/schemas.py
from pydantic import BaseModel
from datetime import datetime

class SChatMessage(BaseModel):
    receiver_id: int
    message: str

    class Config:
        orm_mode = True

class SChatMessageResponse(SChatMessage):
    id: int
    timestamp: datetime