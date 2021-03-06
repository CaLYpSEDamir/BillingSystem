from fastapi import APIRouter
from app.database import db
from app.api.v1.routers.utils import get_user
from app.schemas.transactions import (
    AddMoneyInSchema,
    TransferMoneyEventSchema,
    TransferMoneyInSchema,
    TransferSchema,
    EventEnum,
)
from app.crud import transactions as trans_crud
from app.broker.producer import event_producer

router = APIRouter()


@router.post(
    "/{user_id}/add_money/",
)
async def add_money(user_id: int, body: AddMoneyInSchema):
    """"""
    await get_user(db=db, user_id=user_id)

    transfer = TransferSchema(
        from_user=user_id,
        to_user=user_id,
        amount=body.amount,
    )
    trans_id = await trans_crud.create_transaction(
        db=db, transfer=transfer,
    )

    add_money_event = TransferMoneyEventSchema(
        amount=body.amount,
        type=EventEnum.addition.value,
        from_user=user_id,
        to_user=user_id,
        transaction_id=trans_id,
    )

    await event_producer.send_event(event=add_money_event)
    import asyncio
    # await asyncio.sleep(1)


@router.post(
    "/{user_id}/transfer_money/",
)
async def transfer_money(user_id: int, body: TransferMoneyInSchema):
    """"""
    await get_user(db=db, user_id=user_id)
    await get_user(db=db, user_id=body.to_user)

    transfer = TransferSchema(
        from_user=user_id,
        to_user=body.to_user,
        amount=body.amount,
    )
    trans_id = await trans_crud.create_transaction(
        db=db, transfer=transfer,
    )

    transfer_money_event = TransferMoneyEventSchema(
        amount=body.amount,
        type=EventEnum.transfer.value,
        from_user=user_id,
        to_user=body.to_user,
        transaction_id=trans_id,
    )

    await event_producer.send_event(event=transfer_money_event)
    import asyncio
    # await asyncio.sleep(1)



@router.get(
    "/history/",
    # response_model=List[schemas.User],
)
def history():
    """
    Retrieve users transactions history.
    """
    print('History')
