import math
from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    name: str


# fixme config orm_mode?
class User(UserCreate):
    id: int


class BaseMoney(BaseModel):
    amount: float

    @validator('amount')
    def amount_check(cls, value):
        """"""
        if value < 0:
            return 0
        return math.floor(value * 100) / 100


class AddMoney(BaseMoney):
    pass


class TransferMoney(BaseMoney):
    other_id: int
