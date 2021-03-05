from databases import Database
from typing import Mapping, Optional

from app.models import (
    balances as balances_model,
)


async def get_user_balance(db: Database, user_id: int) -> Optional[Mapping]:
    """Get user's balance."""
    query = balances_model.select().where(balances_model.c.owner == user_id)
    return await db.fetch_one(query)
