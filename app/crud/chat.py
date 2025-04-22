from sqlalchemy.orm import Session
from app.db.models import Chat, Message

# 새로운 채팅 생성
def create_chat(user_id: str, db: Session):
    db_chat = Chat(user_id=user_id, name="New Chat")
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# 특정 user_id의 전체 채팅 목록 조회
def get_chats_by_user_id(user_id: str, db: Session):
    return db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.created_at).all()

# chat_id로 messages 조회
def get_message_by_chat_id(chat_id: str, db: Session):

    results = (
        db.query(Message.question, Message.answer)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    # 결과가 튜플 리스트라면 아래처럼 변환할 수도 있음
    return [{"question": q, "answer": a} for q, a in results]

# 특정 채팅 삭제
def delete_chat_by_id(chat_id: str, db: Session) :
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        return False
    db.delete(chat)
    db.commit()
    return True

# 채팅 이름 변경
def rename_chat_by_id(chat_id: str, new_name: str, db: Session) :
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        return None
    chat.name = new_name
    db.commit()
    db.refresh(chat)
    return chat