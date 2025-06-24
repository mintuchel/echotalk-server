from fastapi import APIRouter
from app.crud.upload import embed_and_upload
from app.schemas.upload import Document

router = APIRouter()

# Pydantic이 각 요소를 Document(title, text) 형태로 파싱해줌
@router.post("/upload-docs")
def upload_docs(docs: list[Document]) :
    embed_and_upload(docs)
    return {"message": "Documents uploaded successfully", "count": len(docs)}