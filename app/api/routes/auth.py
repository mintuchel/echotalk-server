from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserLogin, UserSignUp, UserResponse
from app.crud.user import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Auth"])

# 회원가입
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(request: UserSignUp, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )

    new_user = create_user(db, request)
    return new_user 

# 로그인
@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    
    # 유저 존재 유무 확인
    db_user = get_user_by_email(user.email, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="유저를 찾을 수 없습니다.")
    if not db_user.password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "비밀번호가 올바르지 않습니다.")

    # 쿠키에 사용자 ID 저장 
    # 클라이언트가 브라우저일 경우엔 FastAPI에서 Set-Cookie로 설정한 쿠키를 브라우저가 자동으로 저장하고, 이후 요청에 자동으로 쿠키를 담아서 보내줌
    response.set_cookie(
        key="user_id",
        value=db_user.id,
        httponly=True, # 자바스크립트에서 접근 불가. 보안상 좋아 (XSS 공격에 안전)
        max_age=3600,
        samesite="Lax", # CSRF 공격을 막기 위한 설정
        secure=False # https:// 연결에서만 쿠키를 전송하게 할지 여부. 로컬 개발이라 False로 둬도 됨
    )

    # User 모델 객체지만 Pydantic BaseModel 선언에 의해 UserResponse에 맞춰 자동 변환됨
    return db_user