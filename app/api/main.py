from fastapi import APIRouter, Request, Response
import time
from app.api.routes import auth, chat, message

# 이걸 root에 있는 router에 붙여주면 됨
api_router = APIRouter()

# 성능 모니터링 미들웨어
# @api_router.middleware("http")
# async def performance_middleware(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
    
#     # 응답 헤더에 처리 시간 추가
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

# # 헬스체크 엔드포인트
# @api_router.get("/health")
# async def health_check():
#     return {"status": "healthy", "message": "EchoTalk RAG API is running"}

# 각 라우터 등록
api_router.include_router(chat.router)
api_router.include_router(auth.router)
api_router.include_router(message.router)