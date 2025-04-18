from sqlalchemy.orm import Session
from models import Chat
from schemas import  ChatCreate

def create_chat(db: Session, chat: ChatCreate):
    db_chat = Chat(user_id=chat.user_id, name=chat.name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat_by_id(db:Session, chat_id: str) :
    return db.query(Chat).filter(Chat.id == chat_id).first()