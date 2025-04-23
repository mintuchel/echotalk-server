from fastapi import APIRouter, HTTPException, status, Cookie

from typing import List

from app.schemas.chat import UpdateChatNameRequest, ChatResponse
from app.crud.chat import create_chat, get_chats_by_user_id, delete_chat_by_id, rename_chat_by_id, get_message_by_chat_id
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/chat", tags=["chat"])

# 새로운 채팅 시작
@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def start_new_chat(user_id: str = Cookie(None), db: Session = Depends(get_db)):

    # Cookie 가 없으면
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="쿠키에 user_id가 없습니다.")
    
    try:
        new_chat = create_chat(user_id, db)
        return new_chat
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="create_chat 하면서 터짐")

# 특정 유저의 채팅 목록 조회
@router.get("", response_model=List[ChatResponse], status_code=status.HTTP_200_OK)
def get_chat_list(user_id: str = Cookie(None), db: Session = Depends(get_db)):

    if user_id is None:
        raise HTTPException(status_code=401, detail="쿠키에 user_id가 없습니다.")
    
    try:
        chats = get_chats_by_user_id(user_id, db)
        return chats
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="get_chats_by_user_id 하면서 터짐")

# 특정 채팅의 메시지 조회
# 특정 chat_id의 메시지 기록 보내기
# {
#   "id": "abc-123",
#   "messages": [
#     { "question": "Q1", "answer": "A1" },
#     { "question": "Q2", "answer": "A2" }
#   ]
# }
@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_chat_messages(id: str, user_id: str = Cookie(None), db: Session = Depends(get_db)):

    if user_id is None:
        raise HTTPException(status_code=401, detail="쿠키에 user_id가 없습니다.")
    
    try:
        messages = get_message_by_chat_id(id, db)
        return {"id": id, "messages": messages}
    except Exception as e:
        return {"error": str(e)}

# 특정 채팅 삭제
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_chat(id: str, user_id: str = Cookie(None), db:Session = Depends(get_db)) :
    if user_id is None:
        raise HTTPException(status_code=401, detail="쿠키에 user_id가 없습니다.")
    
    deleted = delete_chat_by_id(id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return deleted

# 특정 채팅 이름 변경
@router.patch("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def rename_chat(request: UpdateChatNameRequest, db: Session = Depends(get_db)):
    chat = rename_chat_by_id(request.id, request.name, db)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat