from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import oauth2, schemas
from ..database import get_db
from ..models import Category, Document


router = APIRouter()


@router.get(
    "/category/", response_model=List[schemas.CategoryShow], tags=["Catalog"]
)
def get_categories(
    db: Session = Depends(get_db),
):
    categories = db.query(Category).all()
    return categories


@router.get(
    "/category/{id}/",
    response_model=schemas.CategoryShow2,
    tags=["Catalog"],
)
def get_category(
    id: int,
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == id).first()
    documents = (
        db.query(Document).filter(Document.category_id == id).all()
    )
    child = db.query(Category).filter(Category.parent_id == id).all()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {
        "title": category.title,
        "subtitle": category.subtitle,
        "description": category.description,
        "image": category.image,
        "documents": documents,
        "child": child,
    }
