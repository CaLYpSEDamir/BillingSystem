import math
from enum import IntEnum
from pydantic import BaseModel, validator


class AddMoneySchema(BaseModel):
    amount: float

    @validator('amount')
    def amount_check(cls, value: float):
        """"""
        if value <= 0:
            raise ValueError('Must be greater than 0.')

        return math.floor(value * 100) / 100


class EventEnum(IntEnum):
    addition = 1
    transfer = 2


# class AddMoneyEventSchema(AddMoneySchema):
class AddMoneyEventSchema(BaseModel):
    type: EventEnum
    owner: int
    amount: float
    transaction_id: int
