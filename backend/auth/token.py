from datetime import datetime, timedelta
from typing import Optional

from database.database import db_dependency
from database.models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class UserAcc(BaseModel):
    email: str
    hashed_password: str

    @classmethod
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    @classmethod
    def authenticate(cls, email: str, password: str, db: db_dependency):
        user_data = db.query(User).filter(User.email == email).first()
        if not user_data:
            return None
        return user_data


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    return {"email": email}
