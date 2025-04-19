from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session

from database import get_db
from models import User
from app.schemas.user import UserCreate, UserResponse, UserLoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

# 회원가입
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 로그인
@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(user: UserLoginRequest, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not user.password==db_user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    # 쿠키에 사용자 ID 저장 
    # 클라이언트가 브라우저일 경우엔 FastAPI에서 Set-Cookie로 설정한 쿠키를 브라우저가 자동으로 저장하고, 이후 요청에 자동으로 쿠키를 담아서 보내줌
    response.set_cookie(key="user_id", value=db_user.id, httponly=True, max_age=3600)

    # User 모델 객체지만 Pydantic BaseModel 선언에 의해 UserResponse에 맞춰 자동 변환됨
    return db_user