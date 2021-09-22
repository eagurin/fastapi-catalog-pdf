import schemas
from database import database
from models import categories, sections


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
        categories.delete(synchronize_session=False).where(categories.c.id == id)
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
