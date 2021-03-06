import math
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, validator


class AmountSchema(BaseModel):
    amount: float

    @validator('amount')
    def amount_check(cls, value: float):
        """Amount must be above 0.
           Make precision 2 digits.
        """
        if value <= 0:
            raise ValueError('Must be greater than 0.')

        return math.floor(value * 100) / 100


class AddMoneyInSchema(AmountSchema):
    pass


class TransferMoneyInSchema(AmountSchema):
    to_user: int


class TransferSchema(AmountSchema):
    from_user: int
    to_user: int


class EventEnum(IntEnum):
    addition = 1
    transfer = 2


class TransferMoneyEventSchema(AmountSchema):
    type: EventEnum
    from_user: int
    to_user: int
    transaction_id: int


class TransactionSchema(BaseModel):
    id: int
    from_user: int
    to_user: int
    amount: float
    state: int
    created: datetime
