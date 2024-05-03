from endpoints.questions import routes as questions_routes
from fastapi import FastAPI

app = FastAPI(
    title="My App",
    docs_url="/swagger",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

app.include_router(questions_routes.router, tags=["Quiz"])
