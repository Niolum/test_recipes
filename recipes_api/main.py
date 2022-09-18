from typing import List
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
import os
from sqlalchemy.orm import Session
from recipes_api import crud, schemas, services
from dotenv import load_dotenv
from .crud import get_db
from fastapi.security import OAuth2PasswordRequestForm
from .database import SessionLocal


load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()



@app.post("/token", response_model=schemas.Token)
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_acces_token(
        data = {"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.UserBase)
def get_user(user: schemas.User = Depends(services.get_current_user)):
    return user


# @app.get("/users/", response_model=List[schemas.UserBase])
# def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

@app.post("/users/{user_id}/recipes/", response_model=schemas.RecipeBase, dependencies=[Depends(get_db)])
def create_recipe_for_user(user_id: int, recipe: schemas.RecipeCreate):
    return crud.create_user_recipe(recipe=recipe, user_id=user_id)

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=400, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/recipes/", response_model=Recipe)
# def create_recipe_for_user(user_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
#     return crud.create_user_recipe(db=db, recipe=recipe, author_id=user_id)


# @app.get("/recipes/", response_model=List[Recipe])
# def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     recipes = crud.get_recipes(db, skip=skip, limit=limit)
#     return recipes