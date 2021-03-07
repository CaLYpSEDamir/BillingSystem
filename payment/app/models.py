import enum

import sqlalchemy as sa

from .database import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("name", sa.String, nullable=False),
)

BALANCES_AMOUNT_CHECK_NAME = 'balances_check_amount_is_not_negative'

balances = sa.Table(
    "balances",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column(
        "owner", sa.Integer, sa.ForeignKey('users.id'),
        nullable=False, unique=True, index=True,
    ),
    sa.Column(
        "amount",
        sa.Float, sa.CheckConstraint(
            'amount>=0', name=BALANCES_AMOUNT_CHECK_NAME,
        ),
        server_default=sa.text("0"), nullable=False,
    ),
)


class TransactionStateEnum(enum.IntEnum):
    """Transaction statuses.

       On transaction creating PENDING status is set.
       On transaction success preparation SUCCESS status is set.
       On money tranferring, if not enough money of user
       NOT_ENOUGH_MONEY status is set.
    """
    PENDING = 1
    SUCCESS = 2
    NOT_ENOUGH_MONEY = 3


transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("from_user", sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
    sa.Column("to_user", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column("amount", sa.Float),
    sa.Column("state", sa.Integer, nullable=False),
    sa.Column("created", sa.DateTime, server_default=sa.sql.func.now(), nullable=False),
)
