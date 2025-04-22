from pydantic import BaseModel
from typing import Optional

class CreateChatRequest(BaseModel):
    user_id: str
    name: Optional[str] = None

class RenameChatRequest(BaseModel) :
    id: str
    new_name: str
    
class ChatResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True