from auth.bearer import (
    Token,
    TokenData,
    create_access_token,
    get_current_user,
)
from auth.utils import hash_password, verify_password
from database.database import db_dependency
from database.models import User
from endpoints.users.models.struct import (
    CreateUser,
    CreateUserResponse,
    UserLogin,
)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/user/login")
async def user_login(user: UserLogin, db: db_dependency):
    """User Log In and Access Token Creation"""

    user_data: User = db.query(User).filter(User.email == user.email).first()
    if not user_data or not verify_password(user.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = TokenData(
        user_id=user_data.id,
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

    hashed_password = hash_password(user.password)
    user = User(
        email=user.email,
        password=hashed_password,
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
