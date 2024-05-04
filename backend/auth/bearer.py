from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "some_random_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES = 45


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    username: str
    email: str
    exp: int | None = None
    token_exiration_date: str | None = None
    location: str | None = "US"


bearer = HTTPBearer()


def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> TokenData:
    token = credentials.credentials
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    decoded_token = decode_jwt_token(token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenData(
        user_id=decoded_token["user_id"],
        email=decoded_token["email"],
        username=decoded_token["username"],
        first_name=decoded_token["first_name"],
        last_name=decoded_token["last_name"],
        date_of_birth=decoded_token["date_of_birth"],
        exp=decoded_token["exp"],
        token_exiration_date=decoded_token["token_expiration_date"],
        location=decoded_token["location"],
    )


def create_access_token(data: TokenData, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    exp_readable = expire.strftime("%Y-%m-%d %H:%M:%S")
    exp_timestamp = int(expire.timestamp())

    to_encode = {
        "user_id": data.user_id,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "date_of_birth": data.date_of_birth,
        "username": data.username,
        "email": data.email,
        "exp": exp_timestamp,
        "token_expiration_date": exp_readable,
        "location": data.location,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

    return encoded_jwt
