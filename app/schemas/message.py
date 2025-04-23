from pydantic import BaseModel
from datetime import datetime

class MessageRequest(BaseModel):
    id: str
    question: str

class MessageResponse(BaseModel) :
    id: str
    chat_id: str
    question: str
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True