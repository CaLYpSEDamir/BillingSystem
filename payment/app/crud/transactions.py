from databases import Database
from app.models import (
    transactions as trans_model,
    TransactionStateEnum as TSE,
)


async def create_adding_transaction(
        db: Database, user_id: int, amount: float,
) -> int:
    """Creating user's money adding transaction."""
    query = trans_model.insert().values(
        owner=user_id,
        amount=amount,
        state=TSE.PENDING.value,
    )
    return await db.execute(query)
