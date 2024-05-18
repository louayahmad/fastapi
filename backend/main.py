from database.database import engine
from database.models import Base
from endpoints.accounts import routes as accounts_routes
from endpoints.transactions import routes as transactions_routes
from endpoints.users import routes as users_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My App",
    docs_url="/swagger",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

# Allow CORS from localhost:3000
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users_routes.router, tags=["Users"])
app.include_router(accounts_routes.router, tags=["Accounts"])
app.include_router(transactions_routes.router, tags=["Transactions"])
