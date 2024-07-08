from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Define database connection parameters
MYSQL_HOST = "postgres_db"
MYSQL_USER = "postgres"
MYSQL_PASSWORD = "postgres"
MYSQL_DB = "banksystem"
MYSQL_PORT = 5432

# Create the SQLAlchemy engine
DATABASE_URL = (
    f"postgresql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)
engine = create_engine(DATABASE_URL)

# Create a sessionmaker to create Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
