
from fastapi import APIRouter
from app.database import db
from app.api.v1.routers.utils import get_user
from app.schemas.transactions import (
    AddMoneySchema,
    AddMoneyEventSchema,
)
from app.crud import transactions as trans_crud
from app.broker.producer import event_producer

router = APIRouter()


@router.post(
    "/{user_id}/add_money/",
)
async def add_money(user_id: int, add: AddMoneySchema):
    """"""
    # fixme maybe needs transaction for db and broker
    await get_user(db=db, user_id=user_id)
    trans_id = await trans_crud.create_adding_transaction(
        db=db, user_id=user_id, amount=add.amount,
    )

    await event_producer.addition_event(
        amount=add.amount,
        user_id=user_id,
        transaction_id=trans_id,
    )


@router.get(
    "/history/",
    # response_model=List[schemas.User],
)
def history():
    """
    Retrieve users transactions history.
    """
    print('History')
