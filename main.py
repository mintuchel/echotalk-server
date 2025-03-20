from fastapi import FastAPI
from pydantic import BaseModel
import requests

from config import OLLAMA_RESTAPI_URL, MODEL_NAME
from models import Question

app = FastAPI()

@app.post("/ask")
async def ask_llm(question: Question) :
    payload = {
        "model" : MODEL_NAME,
        "prompt" : question.prompt,
        "stream" : False
    }

    response = requests.post(OLLAMA_RESTAPI_URL, json=payload)

    if response.status_code == 200 :
        return response.json()
    else :
        return {"error" : "Failed to get response from LLM"}