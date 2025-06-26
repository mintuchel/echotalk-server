from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import configs

# 1. 모든 Model 클래스들이 상속받을 기반 클래스
Base = declarative_base()

# 2. 데이터베이스와 연결할 수 있는 엔진 객체 생성
# engine은 DB 연결을 관리하고 SQL 실행을 전달하는 역할을 함
engine = create_engine(
    configs.mysql_url,
    pool_size = 5,
    max_overflow =0,
    # pool_timeout = 30,
    # pool_recycle=1800
)

# 3. 세션(하나의 DB 트랜잭션 단위) 팩토리 함수
# 트랜잭션이 자동으로 커밋되지 않게 하고 변경 사항을 자동으로 DB에 플러시(반영)하지 않음
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 의존성 주입(Dependency Injection) 할 때 쓰는 함수
def get_mysql():
    db = SessionLocal()
    try:
        # yield를 통해 세션을 라우터로 넘겨줌
        yield db
    finally:
        # 라우터 처리가 끝나면 자동으로 연결 반환
        db.close()