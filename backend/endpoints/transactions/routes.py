from auth.bearer import TokenData, get_current_user
from database.database import db_dependency
from database.models import Account, Transaction, TransactionType, User
from endpoints.transactions.models.struct import (
    DepositFunds,
    DepositFundsResponse,
    WithdrawFunds,
    WithdrawFundsResponse,
)
from endpoints.transactions.statements import create_bank_statement_pdf
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import update

router = APIRouter()


@router.post("/account/withdraw-funds")
async def withdraw_from_account(
    body: WithdrawFunds,
    db: db_dependency,
    _: TokenData = Depends(get_current_user),
) -> WithdrawFundsResponse:
    """Withdraw funds from a user bank account, checking or savings."""

    account = db.query(Account).filter(Account.id == body.account_id).first()
    if not account:
        raise HTTPException(
            status_code=400,
            detail=f"Account with id {body.account_id} not found.",
        )

    if account.balance < body.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds in the account.",
        )

    previous_balance = account.balance
    updated_balance = float(account.balance) - float(body.amount)
    db.execute(
        update(Account)
        .where(Account.id == body.account_id)
        .values(balance=updated_balance)
    )

    db.add(
        Transaction(
            amount=body.amount,
            transaction_type=TransactionType.WITHDRAW.value,
            account_id=account.id,
        )
    )

    db.commit()

    return WithdrawFundsResponse(
        account_id=body.account_id,
        account_type=account.account_type.value,
        previous_balance=previous_balance,
        updated_balance=round(updated_balance, 2),
        transaction_type=TransactionType.WITHDRAW.value,
    )


@router.post("/account/deposit-funds")
async def deposit_into_account(
    body: DepositFunds,
    db: db_dependency,
    _: TokenData = Depends(get_current_user),
) -> DepositFundsResponse:
    """Deposit funds into a user bank account, checking or savings."""

    account = db.query(Account).filter(Account.id == body.account_id).first()
    if not account:
        raise HTTPException(
            status_code=400,
            detail=f"Account with id {body.account_id} not found.",
        )

    previous_balance = account.balance
    updated_balance = float(account.balance) + float(body.amount)
    db.execute(
        update(Account)
        .where(Account.id == body.account_id)
        .values(balance=updated_balance)
    )

    db.add(
        Transaction(
            amount=body.amount,
            transaction_type=TransactionType.DEPOSIT.value,
            account_id=account.id,
        )
    )

    db.commit()

    return DepositFundsResponse(
        account_id=body.account_id,
        account_type=account.account_type.value,
        previous_balance=previous_balance,
        updated_balance=round(updated_balance, 2),
        transaction_type=TransactionType.DEPOSIT.value,
    )


@router.get("/download-statement/")
async def download_pdf(
    db: db_dependency,
    current_user: TokenData = Depends(get_current_user),
):
    """Create a bank statement for a users transactions."""

    transactions = (
        db.query(
            Transaction.amount,
            Transaction.created_at,
            Transaction.transaction_type,
            Account.account_number,
            User.first_name,
            User.last_name,
        )
        .join(
            Account,
            Transaction.account_id == Account.id,
        )
        .join(
            User,
            Account.account_owner_id == User.id,
        )
        .filter(User.id == current_user.user_id)
        .all()
    )

    # Create an object for each transaction
    formatted_transactions = [
        (
            transaction.created_at.strftime("%Y-%m-%d"),
            transaction.transaction_type.value,
            f"${transaction.amount}"
            if transaction.transaction_type.value == "deposit"
            else f"-${transaction.amount}",
            transaction.account_number,
        )
        for transaction in transactions
    ]

    statement = create_bank_statement_pdf(
        f"{current_user.first_name} {current_user.last_name}", formatted_transactions
    )

    return Response(
        content=statement,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sample.pdf"},
    )
