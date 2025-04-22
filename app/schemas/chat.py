from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateChatRequest(BaseModel):
    user_id: str
    name: Optional[str] = None

class RenameChatRequest(BaseModel) :
    chat_id: str
    new_name: str
    
class ChatResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True