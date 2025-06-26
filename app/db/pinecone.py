from pinecone import Pinecone
from app.core.config import configs

def get_pinecone():
    pc = Pinecone(api_key=configs.pinecone_api_key)
    return pc.Index("echoit-vdb")