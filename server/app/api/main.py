from fastapi import APIRouter

from app.api.routes import chat, home

api_router = APIRouter()

# 각 라우터 등록
api_router.include_router(chat.router)
api_router.include_router(home.router)