from typing import Mapping
from databases import Database
from fastapi import HTTPException
from app.crud import users as users_crud


async def get_user(db: Database, user_id: int) -> Mapping:
    """Retrieve user from db.
       If not exist, raise exception.
    """
    user = await users_crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID `{user_id}` is not found."
        )

    return user
