from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from database import engine, Base
import models

app = FastAPI()

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# main 라우터 등록
app.include_router(api_router)