from fastapi import APIRouter, Query, HTTPException, status, Depends

from app.schemas.message import MessageRequest, MessageResponse
from app.crud.message import create_message, get_message_by_chat_id
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/message", tags=["message"])

from app.core.rag import generate_response_with_llm, retrieve_relevant_documents

# 질문에 대한 답변 생성
@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def generate_chat_response(request: MessageRequest, db: Session = Depends(get_db)):

    # pinecone 을 통해 얻어진 결과
    max_score, contexts = retrieve_relevant_documents(request.prompt)

    # 유사도가 작다면
    if max_score < 0.8 :
        print("score too low.. \n asking openai...")
        answer = generate_response_with_llm(request.prompt)
    else :
        print("using Pinecone-based context for OpenAI prompt...")
        answer = generate_response_with_llm(request.prompt, contexts)

    if answer:
        new_message = create_message(request.chat_id, request.prompt, answer, db)
        return new_message
    else :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="openai를 통해 답변 받기 실패"
        )
    
# 특정 chat_id의 메시지 기록 보내기
# {
#   "chat_id": "abc-123",
#   "history": [
#     { "question": "Q1", "answer": "A1" },
#     { "question": "Q2", "answer": "A2" }
#   ]
# }
@router.get("", status_code=status.HTTP_200_OK)
def get_chat_messages(chat_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        messages = get_message_by_chat_id(chat_id, db)
        return {"chat_id": chat_id, "messages": messages}
    except Exception as e:
        return {"error": str(e)}