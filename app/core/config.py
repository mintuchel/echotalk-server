from pydantic_settings import BaseSettings

class Configurations(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    
    class Config:
        env_file = ".env"

configs = Configurations()