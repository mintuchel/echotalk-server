from datetime import datetime
from app.db.connection import get_connection

def get_history_by_date(date: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT question, answer FROM history WHERE date = %s"
    cursor.execute(query, (date,))
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records

def save_to_mysql(question: str, answer: str):
    conn = get_connection()
    cursor = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")
    query = "INSERT INTO history (date, question, answer) VALUES (%s, %s, %s)"
    values = (today_date, question, answer)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
