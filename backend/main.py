from database.database import engine
from database.models import Base
from endpoints.users import routes as users_routes
from fastapi import FastAPI

app = FastAPI(
    title="My App",
    docs_url="/swagger",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

Base.metadata.create_all(bind=engine)

app.include_router(users_routes.router, tags=["Users"])
