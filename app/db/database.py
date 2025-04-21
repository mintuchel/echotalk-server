from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pinecone import Pinecone
from app.core.config import configs

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/echotalk"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_pinecone() :
    pc = Pinecone(api_key = configs.pinecone_api_key)
    return pc.Index("echoit-vdb")