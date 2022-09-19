from . import models, schemas
from pytils.translit import slugify

from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import main



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).filter(models.User.is_blocked == False).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = main.services.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_username(db: Session, username: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    db_user.username = user.username
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, username: str):
    db.delete(get_user_by_name(db, username=username))
    db.commit()
    return {'message': f"Successfully deleted {username}"}


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
    return db.query(models.Recipe).filter(models.Recipe.is_blocked == False).order_by(desc(models.Recipe.created_on), desc(models.Recipe.like), models.Recipe.name).offset(skip).limit(limit).all()


def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def create_user_recipe(db: Session, recipe: schemas.RecipeCreate, user_id: int, category_id: int):
    db_recipe = models.Recipe(**recipe.dict(), author_id=user_id, category_id=category_id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def update_recipe(db: Session, name: str, recipe: schemas.RecipeUpdate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.name == name).first()
    db_recipe.name = recipe.name
    db_recipe.description = recipe.description
    db_recipe.coocking_steps = recipe.coocking_steps
    db_recipe.set_hashtag = recipe.set_hashtag
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, name: str):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.name == name).first()
    db.delete(db_recipe)
    db.commit()
    return {'message': f"Successfully deleted {name}"}
