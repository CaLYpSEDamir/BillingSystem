from typing import List

from fastapi import APIRouter, HTTPException

from app.api.v1.routers.utils import get_user
from app.broker.producer import event_producer
from app.crud import transactions as trans_crud
from app.database import db
from app.schemas.transactions import (AddMoneyInSchema, EventEnum,
                                      TransactionSchema,
                                      TransferMoneyEventSchema,
                                      TransferMoneyInSchema, TransferSchema)

router = APIRouter()


@router.post(
    "/{user_id}/add_money/",
)
async def add_money(user_id: int, body: AddMoneyInSchema):
    """Add money to user's balance."""
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


@router.post(
    "/{user_id}/transfer_money/",
)
async def transfer_money(user_id: int, body: TransferMoneyInSchema):
    """Transfer money from user to another one."""
    if user_id == body.to_user:
        raise HTTPException(
            status_code=400,
            detail="User cannot transfer money to himself."
        )

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


@router.get(
    "/{user_id}/history/",
    response_model=List[TransactionSchema],
)
async def transactions_history(
        user_id: int,
        limit: int = 50,
        offset: int = 0,
):
    """
    Get user's transactions history.
    """
    await get_user(db=db, user_id=user_id)
    return await trans_crud.list_transactions(
        db=db, user_id=user_id, limit=limit, offset=offset,
    )
