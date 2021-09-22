from typing import List
from pydantic import BaseModel


class SectionBase(BaseModel):
    title: str
    description: str = None


class SectionCreate(SectionBase):
    pass


class Section(SectionBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True





class CategoryBase(BaseModel):
    title: str
    subtitle: str
    description: str


class CategoryCreate(CategoryBase):
    parent_id: int = 0

    class Config:
        orm_mode = True


class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int
    sections: List[Section] = []

    class Config:
        orm_mode = True


class SectionCategory(SectionBase):
    id: int
    category_id: CategoryInDB

    class Config:
        orm_mode = True
