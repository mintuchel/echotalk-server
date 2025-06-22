from typing import List

from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.db.database import get_pinecone
from app.core.config import configs
from app.core.prompt_template import contextual_prompt

llm = ChatOpenAI(
    api_key = configs.openai_api_key,
    model_name = "gpt-4o-mini",
    temperature = 0.2, # 사실에 기반한 답변에 집중
)

def rag_qa(question: str) -> str:
    # pinecone 을 통해 얻어진 결과
    max_score, contexts = retrieve_relevant_documents(question)

    # 유사도가 작다면
    if max_score < 0.8 :
        print("score too low.. \n asking openai...")
        answer = generate_response_with_llm(question)
    else :
        print("using Pinecone-based context for OpenAI prompt...")
        answer = generate_response_with_llm(question, contexts)
    
    return answer

def retrieve_relevant_documents(question: str):
    conn = get_pinecone()
    embedding = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)
    vectordb = PineconeVectorStore(index=conn, embedding=embedding)

    query_result = vectordb.similarity_search_with_score(query=question, k=5)

    if not query_result:
        return 0.0, []

    # 문서 내용 추출 및 정제
    contexts = [
        doc.page_content.replace("\n", "")[:500]
        for doc, _ in query_result
    ]

    # 최고 점수 계산
    max_score = max(score for _, score in query_result)

    # 로깅 (선택적)
    for i, (doc, score) in enumerate(query_result):
        print(f"[{i+1}] Score: {score:.4f} | Title: {doc.metadata.get('title', 'Untitled')}")
        print(doc.page_content.replace("\n", "")[:500], "...\n")

    return max_score, contexts

def generate_response_with_llm(question: str, contexts: List[str] = None) -> str :
    if contexts:
        context_text = "\n\n".join(contexts[:5])  # 상위 3개만 사용
        prompt = contextual_prompt(context_text, question)
    else:
        prompt = question

    # llm.invoke 는 동기 함수라 await 처리안해줘도 된다
    # return type은 AIMessage 객체이고 그 중에 content field를 추출해주면 답변만 추출가능
    response = llm.invoke(prompt)
    return response.content