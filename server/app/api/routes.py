# app/api/routes.py
from fastapi import APIRouter
from datetime import datetime
import requests

from app.models.schema import QuestionDTO, ResponseDTO
from app.core.config import OLLAMA_RESTAPI_URL, MODEL_NAME
from app.crud.history import save_to_mysql, get_history_by_date

router = APIRouter()

@router.get("/")
def home():
    return "Hello World!"

@router.get("/history/{date}")
def get_history(date: str):
    try:
        records = get_history_by_date(date)
        return {"date": date, "history": records}
    except Exception as e:
        return {"error": str(e)}

@router.post("/ask", response_model=ResponseDTO)
async def ask_llm(question: QuestionDTO):
    payload = {
        "model": MODEL_NAME,
        "prompt": question.prompt,
        "stream": False
    }

    answer = query_chromadb(question.prompt)
    if answer:
        save_to_mysql(question.prompt, answer)
        return ResponseDTO(created_at=datetime.now().isoformat(), response=answer)

    response = requests.post(OLLAMA_RESTAPI_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        save_to_mysql(question.prompt, data.get("response"))
        return ResponseDTO(
            created_at=data.get("created_at"),
            response=data.get("response")
        )
    return {"error": "Failed to get response from LLM"}
