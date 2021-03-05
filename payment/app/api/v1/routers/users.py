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
    # return await get_user(db=db, user_id=user_id)
    from app.models import users
    async with db.transaction():
        q = users.select(for_update=True).where(users.c.id == 1)
        p(q)
        r = await db.fetch_one(q)
        print(type(r))
        print(r['name'])

        # u = users.update().where(users.c.id == user_id).values(name='asd')
        # p(u)
        import asyncio
        # await asyncio.sleep(20)
        # await db.execute(u)
