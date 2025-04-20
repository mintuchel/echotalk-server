from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Message

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