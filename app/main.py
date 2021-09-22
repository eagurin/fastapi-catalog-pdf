from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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


@app.get("/categories/", response_model=List[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 100):
    return await crud.get_categories(skip=skip, limit=limit)


@app.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate):
    db_category = await crud.get_category_by_title(title=category.title)
    if db_category:
        raise HTTPException(status_code=400, detail="Title already registered")
    return await crud.create_category(category=category)


@app.get("/categories/{id}", response_model=schemas.Category)
async def read_category(id: int):
    db_category = await crud.get_category(category_id=id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.delete("/categories/{id}", status_code=status.HTTP_200_OK)
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
async def update(id: int, r: schemas.Category, db: Session = Depends(get_db)):
    tmp = dict()
    if r.title:
        tmp.update({"title": r.title})
    if r.subtitle:
        tmp.update({"subtitle": r.subtitle})
    if r.description:
        tmp.update({"description": r.description})
    db.query(models.categories).filter(models.categories.c.id == id).update(
        tmp
    )
    db.commit()
    return "Category has been update"


@app.post("/categories/{id}/sections/", response_model=schemas.Section)
async def create_section_for_category(id: int, section: schemas.SectionCreate):
    return await crud.create_category_section(section=section, category_id=id)


@app.get("/sections/", response_model=List[schemas.Section])
async def read_sections(skip: int = 0, limit: int = 100):
    return await crud.get_sections(skip=skip, limit=limit)


@app.get("/sections/{section_id}", response_model=schemas.SectionCategory)
async def read_section(section_id: int):
    return await crud.get_section_category(pk=section_id)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = crud.fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    user = schemas.UserInDB(**user_dict)
    hashed_password = crud.fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: models.User = Depends(crud.get_current_active_user),
):
    return current_user
