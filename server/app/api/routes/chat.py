from fastapi import APIRouter
from datetime import datetime
import requests

from app.models.schema import QuestionDTO, ResponseDTO
from app.core.config import OLLAMA_RESTAPI_URL, MODEL_NAME
from app.crud.conversation import create_conversation, get_conversation_by_date, get_conversation_dates
from langchain_openai import ChatOpenAI

router = APIRouter(prefix="/chat", tags=["chat"])

def ask_openai(prompt: str) :
    llm = ChatOpenAI(
        api_key="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",
        model_name="gpt-4o-mini",
        temperature=0.8,
    )

    # llm.invoke 는 동기 함수라 await 처리안해줘도 된다
    # return type은 AIMessage 객체이고 그 중에 content field를 추출해주면 답변만 추출가능
    answer = llm.invoke(prompt)
    print(answer.content)
    return answer.content

@router.get("/")
def home():
    return "Hello World!"

@router.post("", response_model=ResponseDTO)
def ask_llm(question: QuestionDTO):

    answer = ask_openai(question.prompt)

    if answer:
        create_conversation(question.prompt, answer)
        return ResponseDTO(created_at=datetime.now().isoformat(), response=answer)
    else :
        return {"error": "Failed to get response from LLM"}

# 날짜들을 json 형식으로 return
@router.get("/dates")
def get_chat_dates():
    try:
        date_list = get_conversation_dates()
        return {"dates": date_list}
    except Exception as e:
        return {"error": str(e)}


@router.get("/{date}")
def get_chat_history(date: str):
    try:
        records = get_conversation_by_date(date)
        return {"date": date, "history": records}
    except Exception as e:
        return {"error": str(e)}
