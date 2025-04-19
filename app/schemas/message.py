from pydantic import BaseModel

class MessageRequest(BaseModel):
    chat_id: str
    prompt: str

class MessageResponse(BaseModel) :
    id: str
    chat_id: str
    question: str
    response: str
    created_at: str

    class Config:
        orm_mode = True