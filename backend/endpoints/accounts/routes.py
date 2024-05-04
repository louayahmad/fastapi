from typing import List

from auth.bearer import TokenData, get_current_user
from auth.utils import generate_random_number
from database.database import db_dependency
from database.models import Account
from endpoints.accounts.models.struct import (
    AccountInfo,
    CreateAccount,
    CreateAccountResponse,
    TotalAccounts,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_

router = APIRouter()


@router.get("/get-all-user-accounts")
async def get_all_user_accounts(
    db: db_dependency,
    current_user: TokenData = Depends(get_current_user),
):
    """Get a users bank accounts including checking and savings."""

    accounts = (
        db.query(Account)
        .filter(
            Account.account_owner_id == current_user.user_id,
        )
        .all()
    )

    user_accounts: List[AccountInfo] = []
    balance_of_all_accounts: float = 0
    if accounts:
        for account in accounts:
            balance_of_all_accounts = balance_of_all_accounts + account.balance
            user_accounts.append(
                AccountInfo(
                    id=account.id,
                    account_number=account.account_number,
                    account_type=account.account_type.value,
                    balance=account.balance,
                    account_owner_first_name=account.owner.first_name,
                    account_owner_last_name=account.owner.last_name,
                )
            )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No accounts were found for user "
            f"{current_user.first_name} {current_user.last_name}",
        )

    return TotalAccounts(
        accounts=user_accounts,
        balance_of_all_accounts=balance_of_all_accounts,
    )


@router.post("/create-user-account")
async def create_user_account(
    body: CreateAccount,
    db: db_dependency,
    current_user: TokenData = Depends(get_current_user),
):
    """Create a new user bank account, checking or savings."""

    existing_account = (
        db.query(Account)
        .filter(
            and_(
                Account.account_owner_id == current_user.user_id,
                Account.account_type == body.account_type,
            )
        )
        .first()
    )
    if existing_account:
        raise HTTPException(
            status_code=400,
            detail=f"User already has a {body.account_type} account.",
        )

    last_account = db.query(Account).order_by(Account.id.desc()).first()
    if last_account:
        last_account_number = last_account.account_number
        account_number = last_account_number + 1
    else:
        account_number = generate_random_number()

    db.add(
        Account(
            account_number=account_number,
            balance=body.initial_deposit,
            account_type=body.account_type,
            account_owner_id=current_user.user_id,
        )
    )
    db.commit()

    return CreateAccountResponse(
        account_number=account_number,
        balance=body.initial_deposit,
    )
