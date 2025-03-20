from fastapi import FastAPI
import requests

from config import OLLAMA_RESTAPI_URL, MODEL_NAME
from server.models import QuestionDTO, ResponseDTO

# 서버 실행
app = FastAPI()

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