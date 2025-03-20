from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

from config import OLLAMA_RESTAPI_URL, MODEL_NAME
from models import QuestionDTO, ResponseDTO

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

@app.get("/")
def home() :
    return "Hello World!"


@app.post("/ask", response_model = ResponseDTO)
async def ask_llm(question: QuestionDTO) :
    payload = {
        "model" : MODEL_NAME,
        "prompt" : question.prompt,
        "stream" : False
    }

    response = requests.post(OLLAMA_RESTAPI_URL, json=payload)

    if response.status_code == 200 :
        data = response.json()
        return ResponseDTO(
            created_at = data.get("created_at"),
            response = data.get("response")
        )
    else :
        return {"error" : "Failed to get response from LLM"}