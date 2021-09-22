from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, database, engine, metadata

metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate):
    db_category = await crud.get_category_by_title(title=category.title)
    if db_category:
        raise HTTPException(status_code=400, detail="Title already registered")
    return await crud.create_category(category=category)


@app.get("/categories/", response_model=List[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 100):
    return await crud.get_categories(skip=skip, limit=limit)


@app.get("/categories/{category_id}", response_model=schemas.Category)
async def read_category(category_id: int):
    db_category = await crud.get_category(category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.delete("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def destroy(id: int, db: Session = Depends(get_db)):
    db_category = (
        db.query(models.categories)
        .filter(models.categories.c.id == id)
        .first()
    )
    if db_category:
        db.query(models.categories).filter(
            models.categories.c.id == id
        ).delete(synchronize_session=False)
        db.commit()
        return "Category has been removed"
    raise HTTPException(status_code=404, detail="Category not found")


@app.put("/categories/{id}")
async def update(
    id: int, r: schemas.Category, db: Session = Depends(get_db)
):
    # db_category = (
    #     db.query(models.categories)
    #     .filter(models.categories.c.id == id)
    #     .first()
    # )
    # if db_category:
    db.query(models.categories).filter(
        models.categories.c.id == id
    ).update(
        title=r.title,
        subtitle=r.subtitle,
        description=r.description,
        parent_id=r.parent_id
    )
    db.commit()
    return "Category has been update"
    # raise HTTPException(status_code=404, detail="Category not found")


@app.post(
    "/categories/{category_id}/sections/", response_model=schemas.Section
)
async def create_section_for_category(
    category_id: int, section: schemas.SectionCreate
):
    return await crud.create_category_section(
        section=section, category_id=category_id
    )


@app.get("/sections/", response_model=List[schemas.Section])
async def read_sections(skip: int = 0, limit: int = 100):
    return await crud.get_sections(skip=skip, limit=limit)


@app.get("/sections/{section_id}", response_model=schemas.SectionCategory)
async def read_section(section_id: int):
    return await crud.get_section_category(pk=section_id)
