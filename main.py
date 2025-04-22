from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.db.database import engine
import app.db.models as models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 기본적인 네트워킹 허용범위 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True, # Cookie 허용
    allow_methods=["*"],
    allow_headers=["*"],
)

# main 라우터 등록
app.include_router(api_router)