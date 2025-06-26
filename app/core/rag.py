from typing import List

from app.core.chain import rag_chain

def get_rag_response(question: str) -> str:
    try:
        answer = rag_chain.rag_qa(question)
        return answer
        
    except Exception as e:
        print(f"Error in get_rag_response: {e}")
        return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."