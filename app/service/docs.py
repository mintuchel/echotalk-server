import time
from uuid import uuid4
from app.db.pinecone import get_pinecone
from app.schemas.docs import Document

from app.service.utils import split_text, embedder

def embed_and_upload(documents: list[Document], batch_size: int = 50):

    texts, metadatas, count = [], [] , 1

    # 한개의 문서에 대해
    for doc in documents:
        metadata = {
            "id": str(uuid4()),
            "title": doc.title
        }

        # 한개의 문서를 text_splitter로 chunck들로 나누기
        text_chunks = split_text(doc.text)

        for i, chunk in enumerate(text_chunks):
            metadatas.append({"chunck":i, "text":chunk, **metadata})
            texts.append(chunk)
            count+=1

            if count >= batch_size:
                upload_batch(texts, metadatas)
                texts, metadatas, count = [], [], 1

    if texts:
        upload_batch(texts, metadatas)

def upload_batch(texts, metadatas):

    index = get_pinecone()
    
    try:
        ids = [str(uuid4()) for _ in texts]
        # texts 들을 모두 벡터로 변환하기
        embeds = embedder.embed_documents(texts)
        # 세 개의 리스트를 하나의 tuple로 묶어주기
        index.upsert(vectors=zip(ids, embeds, metadatas))
        print(f"Upserted: {len(texts)} vectors")
    except Exception as e:
        print(f"Error during upsert: {e}")
        time.sleep(1)

def delete_all() :
    index = get_pinecone()
    index.delete(delete_all=True)