from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from app.db.database import get_pinecone
from app.core.config import configs
from app.core.prompt_template import contextual_prompt

def retrieve_relevant_documents(question: str):

    embedding_model = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)
    query_vector = embedding_model.embed_query(question)

    pinecone_index = get_pinecone()

    results = pinecone_index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True,
        include_values=False
    )

    # 문서들을 담아 보낼 context
    contexts = []
    max_score = 0.0

    for match in results['matches']:
        print(f"Score: {match['score']}")
        print(f"Text: {match['metadata']['text']}")
        
        contexts.append(match['metadata']['text'])
        max_score = max(max_score, match['score'])

    if max_score < 0.8:
        return []
    
    return contexts

def get_rag_response(question: str) -> str:
    docs = retrieve_relevant_documents(question)

    if not docs :
        prompt = question
    else :
        context_text = "\n\n".join(docs[:3])
        prompt = contextual_prompt(context_text, question)

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