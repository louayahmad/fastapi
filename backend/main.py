from typing import Annotated

from database.database import Base, SessionLocal, engine
from endpoints.questions import routes as questions_routes
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI(
    title="My App",
    docs_url="/swagger",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(questions_routes.router, tags=["Quiz"])
