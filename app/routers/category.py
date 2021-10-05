from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import oauth2, schemas
from ..crud import delete_file, upload_image
from ..database import get_db
from ..models import Category

router = APIRouter()


@router.post(
    "/categories", status_code=status.HTTP_201_CREATED, tags=["Category"]
)
def create_categories(
    title: str,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    image_file: UploadFile = File(None),
    parent_id: Optional[int] = None,
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
    "/categories", status_code=status.HTTP_202_ACCEPTED, tags=["Category"]
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
    category = db.query(Category).filter(Category.id == id)
    tmp = {}
    if title:
        tmp.update({"title": title})
    if subtitle:
        tmp.update({"subtitle": subtitle})
    if description:
        tmp.update({"description": description})
    if image_file:
        delete_file(category.first().image)
        tmp.update({"image": upload_image(image_file)})
    if parent_id:
        tmp.update({"parent_id": parent_id})
    if not category.first():
        raise HTTPException(status_code=404, detail="Category not found")
    category.update(tmp)
    db.commit()
    return "Category has been update"


@router.get(
    "/categories", response_model=List[schemas.CategoryShow], tags=["Category"]
)
def get_categories(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    categories = db.query(Category).all()
    return categories


@router.get(
    "/categories/{id}", response_model=schemas.CategoryShow, tags=["Category"]
)
def get_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
