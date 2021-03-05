import datetime
import uuid
import enum

import sqlalchemy as sa
from sqlalchemy import (
    DateTime, Column, ForeignKey, Integer, String, Enum, Float, CheckConstraint,
    DefaultClause,
)
from sqlalchemy.orm import relationship

from .database import Base, metadata


# class Users(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#
#
# users = Users.__table__

# class Balances(Base):
#     __tablename__ = "balances"
#
#     id = Column(Integer, primary_key=True, index=True)
#     owner = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
#     amount = Column(Float, CheckConstraint('amount>=0'), default=0, nullable=False)


# class TransactionStateEnum(enum.Enum):
#     new = 1
#     canceled = 2
#     synced = 3
#     fixed = 4
#
#
# def generate_uuid() -> str:
#     return str(uuid.uuid4())


# class Transactions(Base):
#     __tablename__ = "transactions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     owner = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
#     other = Column(Integer, ForeignKey('users.id'), nullable=False)
#     amount = Column(Float, nullable=False)
#     uuid = Column(String, default=generate_uuid, nullable=False)
#     state = Column(Enum(TransactionStateEnum), nullable=False)
#     created = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("name", sa.String, nullable=False),
)

balances = sa.Table(
    "balances",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column(
        "owner", sa.Integer, sa.ForeignKey('users.id'),
        nullable=False, unique=True, index=True,
    ),
    sa.Column(
        "amount", sa.Float, sa.CheckConstraint('amount>=0'),
        server_default=sa.text("0"), nullable=False,
    ),
)


class TransactionStateEnum(enum.IntEnum):
    """"""
    PENDING = 1
    SUCCESS = 2
    CANCELED = 2
    LOST = 4


transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("owner", sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
    # sa.Column("other", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column("amount", sa.Float),
    sa.Column("state", sa.Integer, nullable=False),
    sa.Column("created", sa.DateTime, server_default=sa.sql.func.now(), nullable=False),
)
