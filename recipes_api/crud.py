from . import models, schemas
from pytils.translit import slugify

from sqlalchemy.orm import Session

from . import main



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = main.services.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    slug = slugify(category.name)
    db_category = models.Category(name=category.name, slug=slug)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Recipe).offset(skip).limit(limit).all()


def create_user_recipe(db: Session, recipe: schemas.RecipeCreate, user_id: int, category_id: int):
    db_recipe = models.Recipe(**recipe.dict(), author_id=user_id, category_id=category_id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


