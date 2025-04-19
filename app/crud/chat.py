from sqlalchemy.orm import Session
from models import Chat
from schemas.chat import CreateChatRequest

# 새로운 채팅 생성
def create_chat(chat: CreateChatRequest, db: Session):
    db_chat = Chat(user_id=chat.user_id, name=chat.name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# 특정 user_id의 전체 채팅 목록 조회
def get_chats(user_id: str, db: Session):
    return db.query(Chat).filter(Chat.user_id == user_id).all()