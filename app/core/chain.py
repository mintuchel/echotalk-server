from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA

from app.db.database import get_pinecone
from app.core.config import configs

class RAGChain:
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=configs.openai_api_key,
            model_name="gpt-4o-mini",
            temperature=0.2
        )

        conn = get_pinecone()
        self.embedding = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)
        self.vectordb = PineconeVectorStore(index=conn, embedding=self.embedding)

        self.retriever = self.vectordb.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.8}
        )

    def rag_qa(self, question: str, similarity_threshold: float = 0.8) -> str:
        try:
            docs = self.retriever.get_relevant_documents(question)

            for i, doc in enumerate(docs):
                print(f"[Doc {i+1}] {doc.page_content[:100]}...")  # 앞 100자만 출력

            # 문서가 없을 경우 fallback으로 LLM 단독 호출
            if not docs:
                response = self.llm.invoke(question)
                return response.content if hasattr(response, "content") else str(response)

            rag_qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=False
            )
            result = rag_qa_chain.invoke({"query": question})
            return result["result"]

        except Exception as e:
            print(f"Error in rag_qa: {e}")
            return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."

# 싱글톤 인스턴스 생성
rag_chain = RAGChain()