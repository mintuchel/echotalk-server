from typing import List

from langchain_openai import ChatOpenAI

from app.db.pinecone import get_pinecone
from app.service.utils import embedder
from app.core.config import configs
from app.service.prompt_template import contextual_prompt

llm = ChatOpenAI(
    api_key = configs.openai_api_key,
    model_name = "gpt-4o-mini",
    temperature = 0.2, # 사실에 기반한 답변에 집중
)

def retrieve_relevant_documents(question: str):
    index = get_pinecone()
    query_vector = embedder.embed_query(question)

    result = index.query(
        vector = query_vector,
        top_k = 5,
        include_metadata= True
    )
    
    threshold = 0.8

    filtered_matches = [m for m in result["matches"] if m["score"] >= threshold]

    for match in filtered_matches:
        print(f"Score: {match['score']}")
        print(f"Text: {match['metadata'].get('text')}")
    
    return [m["metadata"].get("text", "") for m in filtered_matches]

def generate_response_with_llm(question: str, contexts: List[str] = None) -> str :
    if contexts:
        context_text = "\n\n".join(contexts) 
        prompt = contextual_prompt(context_text, question)
    else:
        prompt = question

    # llm.invoke 는 동기 함수라 await 처리안해줘도 된다
    # return type은 AIMessage 객체이고 그 중에 content field를 추출해주면 답변만 추출가능
    response = llm.invoke(prompt)
    print(response.content)
    return response.content

def rag_qa(question: str) -> str:
    # pinecone 을 통해 얻어진 결과
    contexts = retrieve_relevant_documents(question)

    # 유사도가 작다면
    if not contexts:
        print("score too low.. \n asking openai...")
    else :
        print("using Pinecone-based context for OpenAI prompt...")
    
    answer = generate_response_with_llm(question, contexts)

    if answer :
        return answer
    else :
        return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."