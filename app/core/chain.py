import openai
from pinecone import Pinecone
from typing import List, Dict, Any

from app.db.database import get_pinecone
from app.core.config import configs

class RAGChain:
    
    def __init__(self):
        # OpenAI 클라이언트 설정
        self.client = openai.OpenAI(api_key=configs.openai_api_key)
        
        # Pinecone 클라이언트 설정
        self.pc = Pinecone(api_key=configs.pinecone_api_key)
        self.index = self.pc.Index(configs.pinecone_index_name)

    def rag_qa(self, question: str, similarity_threshold: float = 0.8) -> str:
        """유사도 기반 스마트 질의응답 - 순수 OpenAI + Pinecone 사용"""
        try:
            # 1. 질문을 임베딩으로 변환
            question_embedding = self._get_embedding(question)
            
            # 2. Pinecone에서 유사한 문서 검색
            search_results = self.index.query(
                vector=question_embedding,
                top_k=5,
                include_metadata=True
            )
            
            # 3. 임계값 기반 필터링
            relevant_docs = []
            for match in search_results.matches:
                if match.score >= similarity_threshold:
                    relevant_docs.append(match.metadata.get('text', ''))
            
            # 4. 컨텍스트 구성
            if relevant_docs:
                context = "\n\n".join(relevant_docs)
                prompt = f"""다음 참고 문서를 바탕으로 질문에 답변해주세요:

참고 문서:
{context}

질문: {question}

답변:"""
            else:
                prompt = f"다음 질문에 답변해주세요: {question}"
            
            # 5. OpenAI API 호출
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in rag_qa: {e}")
            return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."
    
    def _get_embedding(self, text: str) -> List[float]:
        """텍스트를 임베딩으로 변환"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []

# 싱글톤 인스턴스 생성
rag_chain = RAGChain() 