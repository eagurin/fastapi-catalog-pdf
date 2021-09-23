from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base

from .database import metadata

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return "<User(id='%s', email='%s', \
                hashed_password='%s', \
                is_active='%s')>" % (
            self.id, self.email, self.hashed_password, self.is_active)


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
