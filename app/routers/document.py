import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import oauth2
from ..database import get_db
from ..models import Document, User


router = APIRouter()


@router.post("/documents/", tags=["Document"])
async def create_document(
    name: str,
    category_id: int,
    fileb: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    if not fileb.filename[-3:].lower() == "pdf":
        raise HTTPException(status_code=415, detail="Unsupported Media Type")
    url = "static/documents/" + str(uuid.uuid4()) + ".pdf"
    with open(url, "wb") as image:
        shutil.copyfileobj(fileb.file, image)
    new_document = Document(name=name, category_id=category_id, url=url)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


@router.delete("/documents/", tags=["Document"])
async def destroy_document(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    document = db.query(Document).filter(Document.id == id)
    if document.first():
        url = document.first().url
        if os.path.isfile(url):
            os.remove(url)
        else:
            raise HTTPException(status_code=404, detail="File not found")
        document.delete(synchronize_session=False)
        db.commit()
        return "Document has been removed"
    raise HTTPException(status_code=404, detail="Document not found")
