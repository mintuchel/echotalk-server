from pydantic import BaseModel

class Document(BaseModel):
    title: str
    text: str