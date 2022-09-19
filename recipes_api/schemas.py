from typing import List, Union, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class CategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    slug: str


class RecipeBase(BaseModel):
    name: str
    description: Union[str, None] = None
    coocking_steps: Union[str, None] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    is_blocked: bool
    category_id: int
    created_on: datetime
    updated_on: datetime
    like: int
    author_id: int 
    photo = Union[Image, None]
    set_hashtag: Union[str, None] = None 
    users: List['User'] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mod = True


class UserCreate(UserBase):
    password: str



class UserUpdate(UserBase):
    username: Optional[str] = None
    

class User(UserBase):
    id: int 
    is_blocked: Optional[bool] = False
    is_superuser: Optional[bool] = False
    favorites: List[Recipe] = []
    recipes: List[Recipe] = []
    disabled: bool
    created_on: datetime
    update_on: datetime

    class Config:
        orm_mode = True
