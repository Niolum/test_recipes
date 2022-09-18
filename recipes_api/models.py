from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

from .database import Base


Base = declarative_base()

class TypeRecipeEnum(enum.Enum):
    salat = 'Салат'
    pervoe = 'Первое'
    vtoroe ='Второе'
    desert = 'Десерт'
    napitok = 'Напиток'
    vipechka = 'Выпечка'


user_recipe = Table('user_recipes', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('recipe_id', ForeignKey('recipes.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String(30), unique=True, nullable= False, index=True, comment='Имя пользователя')
    hashed_password = Column(String, comment='Пароль')
    is_blocked = Column(Boolean, default=False, index=True, comment='Статус: заблокирован или активен')
    is_superuser = Column(Boolean,default=False)
    favorites = relationship('Recipe', secondary=user_recipe, back_populates='users')
    created_on = Column(DateTime(), default=datetime.now, comment='Дата создания')
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='Дата измерерия')
    recipes = relationship('Recipe', back_populates='author')
    disabled = Column(Boolean, comment='Статус: онлайн или нет')

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    author = relationship('User', back_populates='recipes')
    author_id = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime(), default=datetime.now, comment='Дата создания')
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='Дата измерерия')
    name = Column(String(120), comment='Название блюда')
    type_of_recipe = Column(Enum(TypeRecipeEnum), nullable=False)
    description = Column(String, comment='Описание')
    coocking_steps = Column(String, comment='Шаги приготовления')
    photo = Column(String, nullable=True)
    like = Column(Integer, comment='Лайки')
    set_hashtag = Column(String, comment='Набор хэштегов') 
    is_blocked = Column(Boolean, index=True, comment='Статус: заблокирован или активен')
    users = relationship('User', secondary=user_recipe, back_populates='recipes')


