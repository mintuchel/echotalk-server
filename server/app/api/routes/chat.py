from fastapi import APIRouter
from datetime import datetime
from app.core.config import configs

from app.models.schema import QuestionDTO, ResponseDTO
from app.crud.conversation import create_conversation, get_conversation_by_date, get_conversation_dates
from langchain_openai import ChatOpenAI

router = APIRouter(prefix="/chat", tags=["chat"])

def ask_openai(prompt: str) :
    llm = ChatOpenAI(
        api_key = configs.openai_api_key,
        model_name = "gpt-4o-mini",
        temperature = 0.2, # 사실에 기반한 답변에 집중
    )

    # llm.invoke 는 동기 함수라 await 처리안해줘도 된다
    # return type은 AIMessage 객체이고 그 중에 content field를 추출해주면 답변만 추출가능
    response = llm.invoke(prompt)
    print(response.content)
    return response.content

# OpenAI를 활용하여 답변 return
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

# 특정 날짜의 채팅 기록 보내기
@router.get("/{date}")
def get_chat_history(date: str):
    try:
        records = get_conversation_by_date(date)
        return {"date": date, "history": records}
    except Exception as e:
        return {"error": str(e)}
