from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from .database import Base


Base = declarative_base()


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
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='Дата изменерия')
    recipes = relationship('Recipe', back_populates='author')
    disabled = Column(Boolean, comment='Статус: онлайн или нет')


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, unique=True, nullable=False, index=True, comment='Название типа блюда')
    slug = Column(String, unique=True)
    recipes = relationship('Recipe', back_populates='category')


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    author = relationship('User', back_populates='recipes')
    author_id = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime(), default=datetime.now, comment='Дата создания')
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment='Дата изменерия')
    name = Column(String(120), comment='Название блюда')
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship('Category', back_populates='recipes')
    description = Column(String, comment='Описание')
    coocking_steps = Column(String, comment='Шаги приготовления')
    photo = Column(String, nullable=True)
    like = Column(Integer, nullable=True, comment='Лайки')
    set_hashtag = Column(String, nullable=True, comment='Набор хэштегов') 
    is_blocked = Column(Boolean, default=False, index=True, comment='Статус: заблокирован или активен')
    users = relationship('User', secondary=user_recipe, back_populates='recipes')


