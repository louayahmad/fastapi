import enum
from typing import List

from pydantic import BaseModel


class AccountOptions(enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"


class CreateAccount(BaseModel):
    initial_deposit: float = 0
    account_type: str


class CreateAccountResponse(BaseModel):
    account_number: int
    balance: float


class AccountInfo(BaseModel):
    id: str
    account_number: int
    account_type: str
    balance: float
    account_owner_first_name: str
    account_owner_last_name: str


class TotalAccounts(BaseModel):
    accounts: List[AccountInfo]
    balance_of_all_accounts: float
