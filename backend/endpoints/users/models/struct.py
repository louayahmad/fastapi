from pydantic import BaseModel


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    ssn: int
    username: str
    email: str
    password: str


class CreateUserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class GetUserResponse(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    username: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class CreateAccount(BaseModel):
    account_number: int
    balance: float
    account_type: str
    account_owner_id: str


class CreateTransaction(BaseModel):
    amount: float
    transaction_type: str
    account_id: str
