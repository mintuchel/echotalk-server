from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import retrieval
from app.db.database import get_pinecone
from app.core.config import configs
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

class RAGChain:
    
    def __init__(self):
        # LangChain LLM 정의
        self.llm = ChatOpenAI(
            api_key=configs.openai_api_key,
            model_name="gpt-4o-mini",
            temperature=0.2
        )

        conn = get_pinecone()
        self.embedder = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)
        self.vector_store = PineconeVectorStore(index=conn, embedding=self.embedder)

        # LangChain의 체이닝 과정에 쉽게 통합할 수 있도록 Retriever 객체로 변환해주기
        # Retriever 인터페이스를 활용해야 LangChain의 체인에 연결할 수 있다!
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.8}
        )

    def rag_qa(self, question: str) -> str:

        prompt = ChatPromptTemplate.from_messages(
            "Answer the question based on the context:\n\n{context}\n\nQuestion: {input}"
        )

        document_chain = create_stuff_documents_chain(self.llm, prompt)

        retrieval_chain = retrieval.create_retrieval_chain(self.retriever, document_chain)

        response = retrieval_chain.invoke(question)

        print(response)
        # print(response["answer"])


# 싱글톤 인스턴스 생성
rag_chain = RAGChain()