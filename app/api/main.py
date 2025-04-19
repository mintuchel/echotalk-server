from fastapi import APIRouter

from app.api.routes import chat, auth

# 이걸 root에 있는 router에 붙여주면 됨
api_router = APIRouter()

# 각 라우터 등록
api_router.include_router(chat.router)
api_router.include_router(auth.router)