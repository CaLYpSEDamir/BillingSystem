from typing import List
from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas.users import UserCreateSchema, UserSchema
import app.crud.users as users_crud

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserSchema],
)
async def read_users(
        limit: int = 50,
        offset: int = 0,
):
    """Get list of Users."""
    return await users_crud.get_users(db=db, limit=limit, offset=offset)


@router.get(
    "/{user_id}",
    response_model=List[UserSchema],
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403,
            detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
