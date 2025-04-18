# Pydantic의 BaseModel은 입력 데이터 검증 + 정제를 해주는 동시에,
# 그 데이터를 SQLAlchemy 모델로 쉽게 변환할 수 있게 도와주는 중간다리 역할을 해줌.

# BaseModel 객체는 dict처럼 .dict()로 쉽게 변환할 수 있어서, 아래처럼도 즉시 변환가능
# user_data = user.dict()
# user_data["password"] = get_password_hash(user_data["password"])
# new_user = User(**user_data)


from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Config orm_mode = True 이기 때문에
# password 필드가 없어도 db_user를 그대로 UserResponse로 리턴할 수 있음
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        orm_mode = True