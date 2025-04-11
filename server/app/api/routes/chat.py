from fastapi import APIRouter
from datetime import datetime
import requests

from app.models.schema import QuestionDTO, ResponseDTO
from app.core.config import OLLAMA_RESTAPI_URL, MODEL_NAME
from app.crud.conversation import add_conversation, get_conversation_dates, get_conversation_by_date
from langchain_openai import ChatOpenAI

router = APIRouter(prefix="/chat", tags=["chat"])

async def ask_openai(prompt: str) :
    llm = ChatOpenAI(
        api_key="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",
        model_name="gpt-4o-mini",
        temperature=0.8,
    )

    answer = await llm.invoke(prompt)
    return answer

@router.get("/")
def home():
    return "Hello World!"

@router.post("", response_model=ResponseDTO)
async def ask_llm(question: QuestionDTO):

    answer = await ask_openai(question.prompt)

    if answer:
        create_conversation(question.prompt, answer)
        return ResponseDTO(created_at=datetime.now().isoformat(), response=answer)
    else :
        return {"error": "Failed to get response from LLM"}

@router.get("/{date}")
def get_chat_history(date: str):
    try:
        records = get_conversation_by_date(date)
        return {"date": date, "history": records}
    except Exception as e:
        return {"error": str(e)}
