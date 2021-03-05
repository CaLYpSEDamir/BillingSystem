from fastapi import APIRouter
from app.database import db
from app.schemas.balances import BalanceSchema
from app.crud import balances as balances_crud
from app.api.v1.routers.utils import get_user


router = APIRouter()


@router.get(
    "/{user_id}/balance/",
    response_model=BalanceSchema,
)
async def get_balance(user_id: int):
    """
    Retrieve user's balance.
    """
    await get_user(db=db, user_id=user_id)
    return await balances_crud.get_user_balance(db=db, user_id=user_id)
