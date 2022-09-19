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


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RecipeCreate(RecipeBase):
    coocking_steps: Union[str, None] = None


class Recipes(RecipeBase):
    id: int
    is_blocked: Optional[bool] = False
    category_id: int
    created_on: datetime
    updated_on: datetime
    like: Union[int, None] = None
    author_id: int 
    set_hashtag: Union[str, None] = None
    photo: Image = None


class Recipe(Recipes):
    coocking_steps: Union[str, None] = None

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
    recipes: List[RecipeBase] = []

    class Config:
        orm_mode = True


class UserOut(UserBase):
    is_superuser: Optional[bool] = False
    disabled: bool
    favorites: List[Recipe] = []
    created_on: datetime
    update_on: datetime