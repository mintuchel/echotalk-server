from pydantic import BaseModel

class UpdateChatNameRequest(BaseModel) :
    id: str
    name: str
    
class ChatResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True