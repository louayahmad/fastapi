import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AccountType(enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"


class TransactionType(enum.Enum):
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    date_of_birth = Column(String(255))
    ssn = Column(String(255), unique=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="owner")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    account_number = Column(Integer, unique=True, index=True)
    balance = Column(Float, default=0)
    account_type = Column(Enum(AccountType))
    account_owner_id = Column(String(36), ForeignKey("users.id"))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    amount = Column(Float)
    transaction_type = Column(Enum(TransactionType))
    account_id = Column(String(36), ForeignKey("accounts.id"))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    account = relationship("Account", back_populates="transactions")
