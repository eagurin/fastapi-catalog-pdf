from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    title: str
    subtitle: str
    description: str
    image: str
    parent_id: Optional[int] = 0


class CategoryShow(BaseModel):
    title: str
    
    class Config():
        orm_mode = True



class User(BaseModel):
    name: str
    email: str
    password: str


class UserShow(BaseModel):
    name: str
    email: str
    
    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
