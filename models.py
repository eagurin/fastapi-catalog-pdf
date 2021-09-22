from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from database import metadata


categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, unique=True, index=True),
    Column("subtitle", String),
    Column("description", String),
    Column("parent_id", Integer, ForeignKey("categories.id"))
)


sections = Table(
    "sections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, index=True),
    Column("description", String),
    Column("category_id", Integer, ForeignKey("categories.id"))
)
