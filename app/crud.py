from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import schemas
from database import database
from models import categories, sections

fake_users_db = {
    "test": {
        "username": "test",
        "full_name": "user",
        "email": "test@gmail.com",
        "hashed_password": "fakehashed2222",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_category(category_id: int):
    category = dict(
        await database.fetch_one(
            categories.select().where(categories.c.id == category_id)
        )
    )
    list_section = await database.fetch_all(
        sections.select().where(sections.c.category_id == category["id"])
    )
    category.update({"sections": [dict(result) for result in list_section]})
    return category


async def get_category_by_title(title: str):
    return await database.fetch_one(
        categories.select().where(categories.c.title == title)
    )


async def delete_category_by_id(id: int):
    database.fetch_one(
        categories.delete(synchronize_session=False).where(
            categories.c.id == id
        )
    )
    database.commit()
    return "done"


async def get_categories(skip: int = 0, limit: int = 100):
    results = await database.fetch_all(
        categories.select().offset(skip).limit(limit)
    )
    return [dict(result) for result in results]


async def create_category(category: schemas.CategoryCreate):
    db_category = categories.insert().values(
        title=category.title,
        subtitle=category.subtitle,
        description=category.description,
        parent_id=category.parent_id,
    )
    category_id = await database.execute(db_category)
    return schemas.Category(**category.dict(), id=category_id)


async def get_sections(skip: int = 0, limit: int = 100):
    query = sections.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]


async def get_section_category(pk: int):
    section = dict(
        await database.fetch_one(sections.select().where(sections.c.id == pk))
    )
    category = dict(
        await database.fetch_one(
            categories.select().where(
                categories.c.id == section["category_id"]
            )
        )
    )
    section.update({"category": category})
    return section


async def create_category_section(
    section: schemas.SectionCreate, category_id: int
):
    query = sections.insert().values(**section.dict(), category_id=category_id)
    section_id = await database.execute(query)
    return schemas.Section(
        **section.dict(), id=section_id, category_id=category_id
    )


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
