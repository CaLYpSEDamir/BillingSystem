from databases import Database
from typing import List, Optional, Mapping

from app.schemas.users import UserCreateSchema
from app.models import (
    users as users_model,
    balances as balances_model,
)


async def get_users(db: Database, limit: int, offset: int) -> List[Mapping]:
    """Retrieve User rows from db."""
    query = users_model.select().limit(limit).offset(offset)
    return await db.fetch_all(query)


async def create_user(db: Database, user: UserCreateSchema) -> int:
    """Creating user with balance."""
    async with db.transaction():
        user_query = users_model.insert().values(name=user.name)
        user_id = await db.execute(user_query)
        balance_query = balances_model.insert().values(owner=user_id)
        await db.execute(balance_query)
    return user_id


async def get_user(db: Database, user_id: int) -> Optional[Mapping]:
    """Retrieve User row from db."""
    query = users_model.select().where(users_model.c.id == user_id)
    return await db.fetch_one(query)
