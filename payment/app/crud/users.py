from typing import List, Mapping, Optional

from databases import Database

from app.models import users as users_model
from app.schemas.users import UserCreateSchema


async def list_users(db: Database, limit: int, offset: int) -> List[Mapping]:
    """Retrieve user rows."""
    query = users_model.select().limit(limit).offset(offset)
    return await db.fetch_all(query)


async def create_user(db: Database, user: UserCreateSchema) -> int:
    """Creating user instance."""
    user_query = users_model.insert().values(name=user.name)
    user_id = await db.execute(user_query)
    return user_id


async def get_user(db: Database, user_id: int) -> Optional[Mapping]:
    """Retrieve user row."""
    query = users_model.select().where(users_model.c.id == user_id)
    return await db.fetch_one(query)
