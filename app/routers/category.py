from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi import status as sc
from sqlalchemy.orm import Session

from ..crud import delete_file, upload_image
from ..database import get_db
from ..models import Category
from ..oauth2 import get_current_user
from ..schemas import CategoryShow, User


router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/", response_model=CategoryShow, status_code=sc.HTTP_201_CREATED)
def create_category(
    title: str,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    parent_id: Optional[int] = None,
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    u: User = Depends(get_current_user),
):
    response = Category(
        title=title,
        subtitle=subtitle,
        description=description,
        image=upload_image(image_file),
        parent_id=parent_id,
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    return response


@router.put("/{id}/", response_model=CategoryShow, status_code=202)
def edit_categories(
    id: int,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    image_file: UploadFile = File(None),
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db),
    u: User = Depends(get_current_user),
):
    request = db.query(Category).filter(Category.id == id)

    if not request.first():
        raise HTTPException(status_code=404, detail="Category not found")

    response = dict()
    if title:
        response.update({"title": title})
    if subtitle:
        response.update({"subtitle": subtitle})
    if description:
        response.update({"description": description})
    if parent_id:
        response.update({"parent_id": parent_id})
    if image_file:
        delete_file(request.first().image)
        response.update({"image": upload_image(image_file)})

    request.update(response)
    db.commit()

    return request.first()
