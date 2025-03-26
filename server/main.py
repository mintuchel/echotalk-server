from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer  # 임베딩 모델
import requests
import chromadb
import mysql.connector

from config import OLLAMA_RESTAPI_URL, MODEL_NAME
from models import QuestionDTO, ResponseDTO
from datetime import datetime

# MySQL 접속 정보
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "ollamap"
}

# 서버 실행
app = FastAPI()

# CORS 설정 추가
# local vite 클라이언트 서버에서 요청 받을 수 있도록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name = "menu_collection")

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_chromadb(query):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1  # 가장 관련 있는 1개 결과 반환
    )

    print(results)
    
    if results["documents"][0]:  # 유사한 문서가 존재하면 반환
        similarity_score = results["distances"][0][0]

        # 유사도 점수가 낮을수록 정확한 정보
        # if similarity_score < 0.5:
        print(similarity_score)
        return results["metadatas"][0][0]["answer"]
    
    return None

@app.get("/")
def home() :
    return "Hello World!"

@app.get("/history/{date}")
def get_history(date: str):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT question, answer FROM history WHERE date = %s"
        cursor.execute(query, (date,))
        records = cursor.fetchall()

        cursor.close()
        conn.close()

        print(records)
        
        return {"date": date, "history": records}

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

# MySQL에 질문과 답변을 저장하는 함수
def save_to_mysql(question: str, answer: str):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 오늘의 날짜를 한국 시간 기준으로 "YYYY-MM-DD" 형식으로 변환
        today_date = datetime.now().strftime("%Y-%m-%d")

        # 데이터 삽입 쿼리 실행
        query = "INSERT INTO history (date, question, answer) VALUES (%s, %s, %s)"
        values = (today_date, question, answer)
        cursor.execute(query, values)
        
        # 변경사항 저장 및 연결 종료
        conn.commit()
        cursor.close()
        conn.close()
        print("데이터베이스에 저장 완료")
    except mysql.connector.Error as err:
        print(f"데이터베이스 오류: {err}")

@app.post("/ask", response_model = ResponseDTO)
async def ask_llm(question: QuestionDTO) :
    payload = {
        "model" : MODEL_NAME,
        "prompt" : question.prompt,
        "stream" : False
    }

    # 제일 먼저 chromadb한테 물어보기
    answer = query_chromadb(question.prompt)
    
    print(answer)
    
    if answer :
        print("Chroma db 답변")

        # MySQL에 저장
        save_to_mysql(question.prompt, answer)

        return ResponseDTO(
            created_at = datetime.now().isoformat(),
            response = answer
        )
    
    response = requests.post(OLLAMA_RESTAPI_URL, json=payload)

    if response.status_code == 200 :
        data = response.json()

        # MySQL에 저장
        save_to_mysql(question.prompt, data.get("response"))

        return ResponseDTO(
            created_at = data.get("created_at"),
            response = data.get("response")
        )
    else :
        return {"error" : "Failed to get response from LLM"}