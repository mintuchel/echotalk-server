from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserSignUp

# 새로운 유저 생성
def create_user(user: UserSignUp, db: Session):
    new_user = User(
        name = user.name,
        email = user.email,
        password = user.password # 나중에 꼭 해싱처리
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 이메일로 유저 조회
def get_user_by_email(email: str, db:Session):
    return db.query(User).filter(User.email == email).first()