from sqlalchemy.orm import Session
from models import User, Chat
from schemas import UserCreate

# 새로운 유저 생성
def create_user(db: Session, user: UserCreate):
    new_user = User(
        name = user.name,
        email = user.email,
        password = user.password # 실제로는 해싱필요
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 모든 유저 조회하기
def get_all_users(db: Session):
    return db.query(User).all()

# id로 유저 조회
def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()