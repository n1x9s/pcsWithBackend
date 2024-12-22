# backend/chat/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from backend.chat.dao import ChatDAO
from backend.chat.schemas import SChatMessage, SChatMessageResponse
from backend.users.dependencies import get_current_user
from backend.users.models import Users
from backend.users.dao import UserDAO

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/send/{receiver_id}", response_model=SChatMessageResponse)
async def send_message(receiver_id: int, message: SChatMessage, current_user: Users = Depends(get_current_user)):
    if current_user.email != "prodavec@gmail.com" and receiver_id == "prodavec@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only send messages to the seller"
        )
    return await ChatDAO.create_message(current_user.id, receiver_id, message.message)


@router.get("/messages/{other_user_id}", response_model=List[SChatMessageResponse])
async def get_messages(other_user_id: int, current_user: Users = Depends(get_current_user)):
    other_user = await UserDAO.get_user_by_id(other_user_id)
    if current_user.email != "prodavec@gmail.com" and other_user.email != "prodavec@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only chat with the seller"
        )
    return await ChatDAO.get_messages(current_user.id, other_user_id)
