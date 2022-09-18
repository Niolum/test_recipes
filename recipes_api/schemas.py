from typing import List, Union, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class TypeRecipeEnum(str, Enum):
    salat = 'Салат'
    pervoe = 'Первое'
    vtoroe ='Второе'
    desert = 'Десерт'
    napitok = 'Напиток'
    vipechka = 'Выпечка'


class RecipeBase(BaseModel):
    is_blocked: bool
    name: str
    type_of_recipe: Optional[TypeRecipeEnum]
    description: Union[str, None] = None
    coocking_steps: Union[str, None] = None
    photo = Optional[str]
    set_hashtag: Union[str, None] = None 

    class Config:
        arbitrary_types_allowed = True

class RecipeCreate(RecipeBase):
    pass

    # class Config:
    #     arbitrary_types_allowed = True


class Recipe(RecipeBase):
    id: int
    created_on: datetime
    updated_on: datetime
    like: int
    author_id: int 
    users: List['User'] = []

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True


class UserBase(BaseModel):
    username: str
    id: int 
    is_blocked: Optional[bool] = False
    created_on: datetime
    update_on: datetime

    class Config:
        orm_mode = True
    #     arbitrary_types_allowed = True


class Token(BaseModel):
    access_token: str
    token_type: str

    # class Config:
    #     arbitrary_types_allowed = True


class TokenData(BaseModel):
    username: Union[str, None] = None

    # class Config:
    #     arbitrary_types_allowed = True


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mod = True
    #     arbitrary_types_allowed = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    username: Optional[str] = None

    # class Config:
    #     arbitrary_types_allowed = True
    

class User(UserBase):
    
    is_superuser: Optional[bool] = False

    favorites: List[Recipe] = []
    recipes: List[Recipe] = []
    disabled: bool

    class Config:
        orm_mode = True
