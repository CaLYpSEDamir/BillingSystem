from typing import List
from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas.users import (
    UserCreateSchema,
    UserSchema,
)
from app.crud import users as users_crud
from app.api.v1.routers.utils import get_user

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
    return await users_crud.get_users(db=db, limit=limit, offset=offset)


@router.post(
    "/",
    response_model=UserSchema,
    status_code=201,
)
async def create_user_with_balance(user: UserCreateSchema):
    """Create user."""
    # fixme make it in transaction here, decouple user and balance
    user_id = await users_crud.create_user(db=db, user=user)
    return {**user.dict(), 'id': user_id}


def p(query):
    print(query.compile(compile_kwargs={"literal_binds": True}))


@router.get(
    "/{user_id}",
    response_model=UserSchema,
)
async def read_user(user_id: int):
    """Retrieve user."""

    from app.models import balances
    u = balances.update().where(
        balances.c.owner == user_id,
    ).values(amount=-1)

    # u = balances.insert().values(owner=123)

    await db.execute(u)

    # async with db.transaction():
    #     q = users.select(for_update=True).where(users.c.id == 1)
    #     p(q)
    #     r = await db.fetch_one(q)
    #
    #     import asyncio
    #     # await asyncio.sleep(10)
    #
    #     print(type(r))
    #     print(r['name'])
    #
    #     u = users.update().where(users.c.id == user_id).values(name='asd')
    #     # p(u)
    #     import asyncio
    #     # await asyncio.sleep(20)
    #     await db.execute(u)
    #     raise