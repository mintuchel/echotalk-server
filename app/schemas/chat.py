from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateChatRequest(BaseModel):
    user_id: str
    name: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    user_id: str
    name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True