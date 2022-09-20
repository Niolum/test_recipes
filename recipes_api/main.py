from typing import List
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from recipes_api import crud, schemas, services


load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/documentation")



@app.post("/token", response_model=schemas.Token)
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(services.get_db)):
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


@app.post("/register/", response_model=schemas.UserBase)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(services.get_db)):
    db_user = crud.get_user_by_name(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.User)
async def read_me(current_user: schemas.User = Depends(services.get_current_active_user)):
    return current_user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.put("/users/{username}", response_model=schemas.UserUpdate)
def update_username(username: str, user: schemas.UserUpdate, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    return crud.update_username(username=username, user=user, db=db)


@app.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    db_user = crud.get_user_by_name(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, username=username )


@app.post("/categories/", response_model=schemas.CategoryBase)
def create_new_category(category: schemas.CategoryCreate, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    db_category = crud.get_category_by_name(db=db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(db=db, category=category)


@app.post("/users/{user_id}/recipes/", response_model=schemas.RecipeBase)
def create_recipe_for_user(
    category_id: int, 
    user_id: int, 
    recipe: schemas.RecipeCreate, 
    db: Session = Depends(services.get_db), 
    current_user: schemas.User = Depends(services.get_current_active_user)
):
    return crud.create_user_recipe(db=db, recipe=recipe, user_id=user_id, category_id=category_id)


@app.get("/recipes/", response_model=List[schemas.Recipes])
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    recipes = crud.get_recipes(db, skip=skip, limit=limit)
    return recipes


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    db_recipe = crud.get_recipe_by_id(db=db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@app.put("/recipes/{recipe_id}", response_model=schemas.RecipeUpdate)
def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    return crud.update_recipe(recipe_id=recipe_id, recipe=recipe, db=db)


@app.patch("/recipes/{recipe_id}")
def create_like_recipe(recipe_id: int, db: Session = Depends(services.get_db),current_user: schemas.User = Depends(services.get_current_active_user)):
    return crud.create_like_recipe(recipe_id=recipe_id, db=db)


@app.delete("/recipes/{name}")
def delete_recipe(name: str, db: Session = Depends(services.get_db), current_user: schemas.User = Depends(services.get_current_active_user)):
    return crud.delete_recipe(name=name, db=db)