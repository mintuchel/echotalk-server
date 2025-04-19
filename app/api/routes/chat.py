from fastapi import APIRouter, HTTPException, status

from typing import List

from app.schemas.chat import CreateChatRequest, ChatResponse
from app.crud.chat import create_chat, get_chats
from models import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/chat", tags=["chat"])

# 새로운 채팅 시작
@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat_endpoint(request: CreateChatRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.user_id == request.user_id ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="해당 user_id인 유저는 존재하지 않습니다."
        )
    
    try:
        new_chat = create_chat(db, request)
        return new_chat
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="create_chat 하면서 터짐"
        )

# 특정 유저의 채팅 목록 조회
@router.get("/chats", response_model=List[ChatResponse], status_code=status.HTTP_200_OK)
def get_chat_list(user_id: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.user_id == user_id ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="해당 user_id인 유저는 존재하지 않습니다."
        )
    
    try:
        chats = get_chats(user_id, db)
        return chats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="get_chats 하면서 터짐"
        )