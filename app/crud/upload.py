import time
from uuid import uuid4
from langchain.embeddings.openai import OpenAIEmbeddings
from app.db.database import get_pinecone
from app.rag.utils import split_text
from app.schemas.upload import Document
from app.core.config import configs

embedding_model = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)

def embed_and_upload(documents: list[Document], batch_size: int = 100):
    index = get_pinecone()
    texts, metadatas, count = [], [], 0

    for record in documents:
        metadata = {
            "id": str(uuid4()),
            "title": record.title
        }

        text_chunks = split_text(record.text)

        for i, chunk in enumerate(text_chunks):
            metadatas.append({"chunk": i, "text": chunk, **metadata})
            texts.append(chunk)
            count += 1

            if count >= batch_size:
                upload_batch(index, texts, metadatas)
                texts, metadatas, count = [], [], 0

    if texts:
        upload_batch(index, texts, metadatas)

def upload_batch(index, texts, metadatas):
    try:
        ids = [str(uuid4()) for _ in texts]
        embeds = embedding_model.embed_documents(texts)
        index.upsert(vectors=zip(ids, embeds, metadatas))
        print(f"Upserted: {len(texts)} vectors")
        
    except Exception as e:
        print(f"Error during upsert: {e}")
        time.sleep(1)