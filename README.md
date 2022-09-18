# RecipesApi

## Features
- FastAPI (Python 3.8.6)

  - JWT authentication using OAuth2

- PostgreSQL for the database

- SqlAlchemy for ORM

- Alembic for database migrations

## Installation

      git clone https://github.com/Niolum/test_recipes.git

      pip install -r requirements.txt

      put inside the .env file: 

        - DATABASE_URL = 'postgresql://postgres:<password>@localhost/<name_of_the_datbase>'
        - ACCESS_TOKEN_EXPIRE_MINUTES = 30
        - ALGORITHM = HS256
        - SECRET_KEY = 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7

      alembic init alembic

      alembic upgrade head

      alembic revision --autogenerate -m "New Migration"

      uvicorn recipes_api.main:app --reload



