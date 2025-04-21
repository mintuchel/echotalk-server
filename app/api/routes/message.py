from fastapi import APIRouter, Query, HTTPException, status, Depends
from app.core.config import configs
from typing import List

from app.schemas.message import MessageRequest, MessageResponse
from app.crud.message import create_message, get_message_by_chat_id
from langchain_openai import ChatOpenAI
from app.db.database import get_pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/message", tags=["message"])

def ask_openai(question: str, contexts: List[str] = None) -> str :
    if contexts:
        context_text = "\n\n".join(contexts[:3])  # 상위 3개만 사용
        prompt = f"""다음 정보를 참고하여 사용자의 질문에 답하세요.

        ### 문서 정보 ###
        {context_text}

        ### 사용자 질문 ###
        {question}

        ### 답변 ###
        """
    else:
        prompt = question

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

def ask_pinecone(question: str):
    conn = get_pinecone()
    embedding = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)
    vectordb = PineconeVectorStore(index=conn, embedding=embedding)

    query_result = vectordb.similarity_search_with_score(query=question,k=5)

    if not query_result :
        return 0.0, []
    
    # 문서들을 담아 보낼 context
    contexts = []
    max_score = 0.0

    for doc, score in query_result:
        text = doc.page_content.replace("\n", "")[:500]
        title = doc.metadata["title"]

        contexts.append(text)
        max_score = max(max_score, score)

        print(score, title)
        print(text, "....")
        print("\n")
        
    return max_score, contexts

# 질문에 대한 답변 생성
@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def ask_llm(request: MessageRequest, db: Session = Depends(get_db)):

    # pinecone 을 통해 얻어진 결과
    max_score, contexts = ask_pinecone(request.prompt)

    # 유사도가 작다면
    if max_score < 0.8 :
        print("score too low.. \n asking openai...")
        answer = ask_openai(request.prompt)
    else :
        print("using Pinecone-based context for OpenAI prompt...")
        answer = ask_openai(request.prompt, contexts)

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