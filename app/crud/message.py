from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Message

def create_message(question: str, answer: str, db:Session):
    new_message = Message(
        chat_id = 1,
        question = question,
        answer = answer,
    )

    db.add(new_message)
    db.commit()

    # conn = get_connection()
    # cursor = conn.cursor()
    # today_date = datetime.now()
    # query = "INSERT INTO message (created_at, question, answer) VALUES (%s, %s, %s)"
    # values = (today_date, question, answer)
    # cursor.execute(query, values)
    # conn.commit()
    # cursor.close()
    # conn.close()

# 날짜들을 string List 형식으로 return
def get_message_dates(db: Session) :
    
    results = (
        db.query(func.date(Message.created_at).label("dates"))
        .group_by(func.date(Message.created_at))
        .order_by(func.date(Message.created_at).desc())
        .all()
    )

    date_list = [date[0].strftime("%Y-%m-%d") for date in results]
    return date_list

    # conn = get_connection()
    # cursor = conn.cursor()
    # query = "SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS dates FROM message GROUP BY dates ORDER BY dates DESC"
    # cursor.execute(query)
    # records = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # date_list = [row[0] for row in records]
    # return date_list

# 인자인 date 는 "2025-04-10" 같은 문자열
def get_message_by_date(date: str, db:Session):

    results = (
        db.query(Message.question, Message.answer)
        .filter(func.date(Message.created_at) == date)
        .order_by(Message.created_at.asc())
        .all()
    )
    # 결과가 튜플 리스트라면 아래처럼 변환할 수도 있음
    return [{"question": q, "answer": a} for q, a in results]

    # conn = get_connection()
    # cursor = conn.cursor(dictionary=True)

    # # 특정 날짜에 해당하는 채팅내역 조회
    # query = "SELECT question, answer FROM message WHERE DATE(created_at) = %s ORDER BY created_at ASC"
    # cursor.execute(query, (date,))
    # records = cursor.fetchall()

    # cursor.close()
    # conn.close()

    # return records