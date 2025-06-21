from openai import OpenAI

from typing import List

from app.db.database import get_pinecone
from app.core.config import configs
from app.core.prompt_template import contextual_prompt

client = OpenAI(api_key=configs.openai_api_key)

def get_embedding(question:str) -> list:
    response = client.embeddings.create(
        input = question,
        model = 'text-embedding-3-small'
    )
    return response.data[0].embedding

def retrieve_relevant_documents(question: str):

    query_vector = get_embedding(question)

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
 
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature = 0.2
    )

    print(response.output_text)
    return response.output_text