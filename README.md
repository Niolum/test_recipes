# RecipesApi

## Features
- Python (version 3.8.6)

- FastAPI (version 0.85.0)

  - JWT authentication using OAuth2

- PostgreSQL for the database

- SqlAlchemy for ORM (version 1.4.41)

- Alembic for database migrations (version 1.8.1)

## Installation

      git clone https://github.com/Niolum/test_recipes.git

      pip install -r requirements.txt

      in the dev.env file there are parameters for launching as an example:

        - DATABASE_URL
        - ACCESS_TOKEN_EXPIRE_MINUTES
        - ALGORITHM
        - SECRET_KEY

      alembic upgrade head

      uvicorn recipes_api.main:app --reload
     
 Scheme of interaction with the service:
 - http://127.0.0.1:8000/documentation


