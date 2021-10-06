from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import oauth2, schemas
from ..crud import delete_file, upload_image
from ..database import get_db
from ..models import Category


router = APIRouter()


@router.post(
    "/categories/",
    response_model=schemas.CategoryShow,
    status_code=status.HTTP_201_CREATED,
    tags=["Category"],
)
def create_category(
    title: str,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    parent_id: Optional[int] = None,
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    new_category = Category(
        title=title,
        subtitle=subtitle,
        description=description,
        image=upload_image(image_file),
        parent_id=parent_id,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put(
    "/categories/{id}/",
    response_model=schemas.CategoryShow,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Category"],
)
def edit_categories(
    id: int,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    image_file: UploadFile = File(None),
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    request = db.query(Category).filter(Category.id == id)
    if not request.first():
        raise HTTPException(status_code=404, detail="Category not found")
    temp = dict()
    if title:
        temp.update({"title": title})
    if subtitle:
        temp.update({"subtitle": subtitle})
    if description:
        temp.update({"description": description})
    if image_file:
        old_image = request.first().image
        if old_image:
            delete_file(old_image)
        temp.update({"image": upload_image(image_file)})
    if parent_id:
        temp.update({"parent_id": parent_id})
    request.update(temp)
    db.commit()
    return request.first()
