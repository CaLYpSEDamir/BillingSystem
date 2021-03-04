from databases import Database
from typing import List

from app.schemas.users import UserSchema
from app.models import users


async def get_users(db: Database, limit: int, offset: int) -> List[UserSchema]:
    """Retrieve User rows from db."""

    query = users.select().limit(limit).offset(offset)
    return await db.fetch_all(query)
