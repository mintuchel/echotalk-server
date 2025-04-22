from sqlalchemy.orm import Session
from app.db.models import Message

# 새로운 메시지 생성
def create_message(chat_id: str, question: str, answer: str, db:Session):
    new_message = Message(
        chat_id = chat_id,
        question = question,
        answer = answer,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message