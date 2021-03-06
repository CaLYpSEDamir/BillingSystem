from typing import Mapping, Optional

from databases import Database
from app.models import (
    transactions as trans_model,
    TransactionStateEnum as TSE,
)
from app.schemas.transactions import (
    TransferSchema,
)


async def create_transaction(
        db: Database, transfer: TransferSchema,
) -> int:
    """Creating user's money adding transaction."""
    query = trans_model.insert().values(
        from_user=transfer.from_user,
        to_user=transfer.to_user,
        amount=transfer.amount,
        state=TSE.PENDING.value,
    )
    return await db.execute(query)


async def get_transaction(
        db: Database, trans_id: int, for_update=False,
) -> Optional[Mapping]:
    """"""
    query = trans_model.select(for_update=for_update).where(
        trans_model.c.id == trans_id,
    )
    return await db.fetch_one(query)


async def update_state(
        db: Database, trans_id: int, state=TSE,
):
    """"""
    query = trans_model.update().where(
        trans_model.c.id == trans_id,
    ).values(state=state)

    await db.execute(query)
