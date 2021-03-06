from typing import Mapping, Optional

from asyncpg.exceptions import CheckViolationError
from databases import Database

from app.crud import balances as balances_crud
from app.crud import transactions as trans_crud
from app.models import BALANCES_AMOUNT_CHECK_NAME
from app.models import TransactionStateEnum as TSE
from app.schemas.transactions import TransferMoneyEventSchema

TRANS_NOT_FOUND_ERR = 'Transaction with ID {0} is not found.'


async def prepare_adding_money_event(
        db: Database, event: TransferMoneyEventSchema,
):
    """"""
    async with db.transaction():
        locked_trans: Optional[Mapping] = await trans_crud.get_transaction(
            db=db, trans_id=event.transaction_id, for_update=True,
        )
        if locked_trans is None:
            raise Exception(TRANS_NOT_FOUND_ERR.format(event.transaction_id))

        if locked_trans['state'] != TSE.PENDING:
            return

        await balances_crud.update_user_balance(
            db=db, owner=event.from_user, amount=event.amount,
        )

        await trans_crud.update_state(
            db=db, trans_id=event.transaction_id, state=TSE.SUCCESS,
        )


async def prepare_transfer_money_event(
        db: Database, event: TransferMoneyEventSchema,
):
    """"""
    try:
        async with db.transaction():
            locked_trans: Optional[Mapping] = await trans_crud.get_transaction(
                db=db, trans_id=event.transaction_id, for_update=True,
            )
            if locked_trans is None:
                raise Exception(TRANS_NOT_FOUND_ERR.format(event.transaction_id))

            if locked_trans['state'] != TSE.PENDING:
                return

            first_update_query, second_update_query = _order_update_queries(
                from_user=event.from_user,
                to_user=event.to_user,
                amount=event.amount,
            )

            await db.execute(first_update_query)
            await db.execute(second_update_query)

            await trans_crud.update_state(
                db=db, trans_id=event.transaction_id, state=TSE.SUCCESS,
            )

    except Exception as err:
        if type(err) == CheckViolationError and BALANCES_AMOUNT_CHECK_NAME in str(err):
            await trans_crud.update_state(
                db=db, trans_id=event.transaction_id, state=TSE.NOT_ENOUGH_MONEY,
            )
            return
        else:
            raise err


def _order_update_queries(from_user: int, to_user: int, amount: float):
    """Avoiding deadlocks."""
    subtraction_query = balances_crud.amount_update_query(
        owner=from_user, amount=(-1 * amount),
    )

    addition_query = balances_crud.amount_update_query(
        owner=to_user, amount=amount,
    )

    min_ = min(from_user, to_user)
    if from_user == min_:
        first_q = subtraction_query
        second_q = addition_query
    else:
        first_q = addition_query
        second_q = subtraction_query

    return first_q, second_q
