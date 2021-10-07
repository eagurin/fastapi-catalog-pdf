from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: List[EmailStr]


class DocumentsShow(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


class Category(BaseModel):
    title: str
    subtitle: str
    description: str
    image: str
    parent_id: Optional[int] = 0


class CategoryEdit(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True


class ParentCategory(BaseModel):
    title: str
    subtitle: Optional[str] = None
    image: Optional[str] = None
    id: int

    class Config:
        orm_mode = True


class CategoryShow(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True


class CategoryShow2(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    child: List[ParentCategory] = []
    documents: List[DocumentsShow] = []

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserShow(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class FeedbackShow(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True
