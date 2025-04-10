from pydantic import BaseModel

class QuestionDTO(BaseModel):
    prompt: str

class ResponseDTO(BaseModel) :
    created_at: str
    response: str