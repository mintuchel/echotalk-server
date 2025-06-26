from fastapi import APIRouter
from app.service.docs import embed_and_upload, delete_all
from app.schemas.docs import Document

router = APIRouter(prefix="/docs", tags=["Document Management"])

# Pydantic이 각 요소를 Document(title, text) 형태로 파싱해줌
@router.post("")
def upload_docs(docs: list[Document]) :
    embed_and_upload(docs)
    return {"message": "Documents uploaded successfully", "count": len(docs)}

@router.delete("")
def delete_docs():
    delete_all()
    return {"message": "All records deleted"}
