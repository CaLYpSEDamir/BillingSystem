from typing import Mapping, Optional

from databases import Database

from app.models import balances as balances_model


async def create_user_balance(db: Database, user_id: int) -> int:
    """Creating user balance instance."""
    balance_query = balances_model.insert().values(owner=user_id)
    await db.execute(balance_query)
    return user_id


async def get_user_balance(
        db: Database, user_id: int, for_update=False,
) -> Optional[Mapping]:
    """Get user's balance."""
    query = balances_model.select(for_update=for_update).where(
        balances_model.c.owner == user_id,
    )
    return await db.fetch_one(query)


async def update_user_balance(db: Database, owner: int, amount: float):
    """Update user's balance amount value."""
    query = amount_update_query(owner=owner, amount=amount)
    await db.execute(query)


def amount_update_query(owner: int, amount: float):
    """Get user's balance amount value updating query."""
    query = balances_model.update().where(
        balances_model.c.owner == owner,
    ).values(amount=balances_model.c.amount + amount)

    return query
