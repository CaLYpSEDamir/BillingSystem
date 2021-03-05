from pydantic import BaseModel


class BalanceSchema(BaseModel):
    id: int
    owner: int
    amount: float
