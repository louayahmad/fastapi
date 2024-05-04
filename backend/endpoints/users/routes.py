from auth.bearer import Token, TokenData, create_access_token, get_current_user
from database.database import db_dependency
from database.models import User
from endpoints.users.models.struct import (
    CreateUser,
    CreateUserResponse,
    GetUserResponse,
    UserLogin,
)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/user/login")
def user_login(user: UserLogin, db: db_dependency):
    """User Log In and Access Token Creation"""

    user_data: User = db.query(User).filter(User.email == user.email).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = TokenData(
        user_id=str(user_data.id),
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        date_of_birth=user_data.date_of_birth,
        location="US",
    )
    access_token = create_access_token(data=token_data)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
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
