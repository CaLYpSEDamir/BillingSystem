from typing import List

from fastapi import APIRouter

from app.api.v1.routers.utils import get_user
from app.crud import balances as balances_crud
from app.crud import users as users_crud
from app.database import db
from app.schemas.users import UserCreateSchema, UserSchema

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserSchema],
)
async def list_users(
        limit: int = 50,
        offset: int = 0,
):
    """Get list of Users."""
    return await users_crud.list_users(db=db, limit=limit, offset=offset)


@router.post(
    "/",
    response_model=UserSchema,
    status_code=201,
)
async def create_user_with_balance(user: UserCreateSchema):
    """Create user instance."""
    async with db.transaction():
        user_id = await users_crud.create_user(db=db, user=user)
        await balances_crud.create_user_balance(db=db, user_id=user_id)

    return {**user.dict(), 'id': user_id}


@router.get(
    "/{user_id}",
    response_model=UserSchema,
)
async def read_user(user_id: int):
    """Get user information."""
    return await get_user(db=db, user_id=user_id)
