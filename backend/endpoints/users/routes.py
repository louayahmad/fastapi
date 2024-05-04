from database.database import db_dependency
from database.models import User
from endpoints.users.models.struct import CreateUser
from fastapi import APIRouter

router = APIRouter()


@router.post("/create_user/")
async def create_user(user: CreateUser, db: db_dependency):
    """Create a Bank Account User"""

    user = User(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        ssn=user.ssn,
    )

    db.add(user)
    db.commit()
