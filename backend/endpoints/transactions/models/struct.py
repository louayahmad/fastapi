from typing import List

from pydantic import BaseModel


class WithdrawFunds(BaseModel):
    account_id: str
    amount: float


class WithdrawFundsResponse(BaseModel):
    account_id: str
    account_type: str
    previous_balance: float
    updated_balance: float
    transaction_type: str


class DepositFunds(BaseModel):
    account_id: str
    amount: float


class DepositFundsResponse(BaseModel):
    account_id: str
    account_type: str
    previous_balance: float
    updated_balance: float
    transaction_type: str


class TransactionsStruct(BaseModel):
    id: str
    amount: float
    transaction_type: str


class AccountTransactions(BaseModel):
    account_number: int
    account_type: int
    transaction: List[TransactionsStruct]


class Transactions(BaseModel):
    user_id: str
    transactions: List[AccountTransactions]
