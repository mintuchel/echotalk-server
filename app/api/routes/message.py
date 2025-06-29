from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.mysql import get_mysql
from app.schemas.message import MessageRequest, MessageResponse
from app.crud.message import create_message
from app.service.rag import get_rag_response

router = APIRouter(prefix="/message", tags=["Message"])

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def generate_chat_response(request: MessageRequest, db: Session = Depends(get_mysql)):
    # 비동기 RAG 응답 생성
    answer = get_rag_response(request.question)

    if answer:
        new_message = create_message(request.chat_id, request.question, answer, db)
        return new_message
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="openai를 통해 답변 받기 실패"
        )