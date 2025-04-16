import mysql.connector
from pinecone import Pinecone
from app.core.config import configs

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "echotalk"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_pinecone_connection() :
    pc = Pinecone(api_key=configs.pinecone_api_key)
    return pc.Index("echoit-vdb")