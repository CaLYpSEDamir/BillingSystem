from typing import List, Mapping, Optional

from databases import Database
from sqlalchemy import or_

from app.models import TransactionStateEnum as TSE
from app.models import transactions as trans_model
from app.schemas.transactions import TransferSchema


async def list_transactions(
        db: Database, user_id: int, limit: int, offset: int,
) -> List[Mapping]:
    """Retrieve user's transaction rows."""
    query = trans_model.select().where(
        or_(
            trans_model.c.from_user == user_id,
            trans_model.c.to_user == user_id,
        )
    ).limit(limit).offset(offset).order_by(trans_model.c.id)
    return await db.fetch_all(query)


async def create_transaction(
        db: Database, transfer: TransferSchema,
) -> int:
    """Creating money transaction instance."""
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
    """Get transaction row."""
    query = trans_model.select(for_update=for_update).where(
        trans_model.c.id == trans_id,
    )
    return await db.fetch_one(query)


async def update_state(db: Database, trans_id: int, state=TSE):
    """Update transaction's state field value."""
    query = trans_model.update().where(
        trans_model.c.id == trans_id,
    ).values(state=state)

    await db.execute(query)
