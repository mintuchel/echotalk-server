from fastapi import APIRouter
from datetime import datetime
from app.core.config import configs
from typing import List

from app.schema.chat import QuestionDTO, ResponseDTO
from app.crud.message import create_message, get_message_by_date, get_message_dates
from langchain_openai import ChatOpenAI
from app.db.connection import get_pinecone_connection
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings

router = APIRouter(prefix="/chat", tags=["chat"])

def ask_openai(question: str, contexts: List[str] = None) -> str :
    if contexts:
        context_text = "\n\n".join(contexts[:3])  # 상위 3개만 사용 (길이 제한 고려)
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
    conn = get_pinecone_connection()
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

# OpenAI를 활용하여 답변 return
@router.post("", response_model=ResponseDTO)
def ask_llm(question: QuestionDTO):

    # pinecone 을 통해 얻어진 결과
    max_score, contexts = ask_pinecone(question.prompt)

    # 유사도가 작다면
    if max_score < 0.5 :
        print("score too low.. \n asking openai...")
        answer = ask_openai(question.prompt)
    else :
        print("using Pinecone-based context for OpenAI prompt...")
        answer = ask_openai(question.prompt, contexts)

    if answer:
        create_message(question.prompt, answer)
        return ResponseDTO(created_at=datetime.now().isoformat(), response=answer)
    else :
        return {"error": "Failed to get response from LLM"}

# 날짜들을 json 형식으로 return
@router.get("/dates")
def get_chat_dates():
    try:
        date_list = get_message_dates()
        return {"dates": date_list}
    except Exception as e:
        return {"error": str(e)}

# 특정 날짜의 채팅 기록 보내기
@router.get("/{date}")
def get_chat_history(date: str):
    try:
        records = get_message_by_date(date)
        return {"date": date, "history": records}
    except Exception as e:
        return {"error": str(e)}
