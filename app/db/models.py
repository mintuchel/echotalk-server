import uuid
import pytz
from datetime import datetime
from sqlalchemy import Column, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# mysql.py에서 생성한 Base 객체 import
# 모든 Model 클래스들이 상속받을 기반 클래스임
from app.db.mysql import Base

def generate_uuid():
    return str(uuid.uuid4())

def korea_now():
    korea_timezone = pytz.timezone('Asia/Seoul')
    return datetime.now(korea_timezone)

class User(Base):
    __tablename__ = "user_table"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # 일대다 단방향
    # back_populates 에서 backref로 단방향 관계 설정
    # cascade -> user 삭제 시 conversation, message 모두 함께 삭제
    conversations = relationship("Chat", backref="user", cascade="all, delete", passive_deletes=True)

class Chat(Base):
    __tablename__ = "chat"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("user_table.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default = korea_now, nullable=False)

    # 일대다 단방향
    messages = relationship("Message", backref="chat", cascade="all, delete", passive_deletes=True)

class Message(Base):
    __tablename__ = "message"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    chat_id = Column(String(36), ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)
    
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), default = korea_now, nullable=False)