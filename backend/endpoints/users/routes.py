from datetime import timedelta

from auth.token import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    UserAcc,
    create_access_token,
    get_current_user,
)
from database.database import db_dependency
from database.models import User
from endpoints.users.models.struct import (
    CreateUser,
    CreateUserResponse,
    GetUserResponse,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = UserAcc.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: UserAcc = Depends(get_current_user)):
    return current_user


@router.post("/create_user/")
async def create_user(user: CreateUser, db: db_dependency) -> CreateUserResponse:
    """Create a Bank Account User"""

    user = User(
        email=user.email,
        password=user.password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        ssn=user.ssn,
    )

    db.add(user)
    db.commit()

    return CreateUserResponse(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
    )


@router.get("/get_user/")
async def get_user(id: str, db: db_dependency) -> GetUserResponse:
    """Get user from the database"""

    user: User = db.query(User).filter(User.id == id).first()

    if user:
        return GetUserResponse(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            date_of_birth=user.date_of_birth,
        )
    else:
        raise HTTPException(status_code=404, detail="User not found!")
