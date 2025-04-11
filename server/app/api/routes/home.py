from fastapi import APIRouter

router = APIRouter(prefix="/home", tags=["home"])

@router.get("/")
def home():
    return "Hello World!"

@router.get("/{num}")
def home():
    return "num num num"