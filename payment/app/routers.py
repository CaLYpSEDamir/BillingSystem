import json
import uuid
import datetime
import asyncio
from typing import Any, Dict, Union, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from . import schemas
from .database import db, engine
from .broker.producer import aioproducer
from .models import users, balances

# from .models import users, balances, transactions, TransactionStateEnum as TSE

router = APIRouter()


def p(query):
    print(query.compile(compile_kwargs={"literal_binds": True}))


@router.get(
    "/users/",
    tags=["users"],
)
async def get_users(
        limit: int = 50,
        offset: int = 0,
):
    """Get list of Users."""
    query = users.select().limit(limit).offset(offset)
    return await db.fetch_all(query)


@router.post(
    "/users/",
    tags=["users"],
    response_model=schemas.User,
)
async def create_user_with_balance(user: schemas.UserCreate):
    """Create user."""
    async with db.transaction():
        user_query = users.insert().values(name=user.name)
        user_id = await db.execute(user_query)
        balance_query = balances.insert().values(user=user_id)
        await db.execute(balance_query)

    return {**user.dict(), "id": user_id}


@router.get(
    "/users/{user_id}",
    tags=["users"],
    response_model=schemas.User,
)
async def get_user(user_id: int):
    """Get list of Users."""
    # fixme 404 if does not exist
    query = users.select().where(users.c.id == user_id)
    user = await db.fetch_one(query)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    query = balances.select().where(users.c.id == user_id)
    balance = await db.fetch_one(query)
    print(user, balance)


@router.post(
    "/users/{user_id}/add_money2/",
    tags=["balances"],
)
async def add_money2(
        user_id: int,
        addition: schemas.AddMoney,
):
    """"""
    print(addition, user_id)
    if addition.amount <= 0:
        # fixme here needs validation message
        return
    # fixme problems with default values
    query = transactions.insert().values(
        owner=user_id,
        other=user_id,
        amount=addition.amount,
        uuid=str(uuid.uuid4()),
        state=TSE.new,
        # created=datetime.datetime.utcnow(),
    )
    await db.execute(query)


@router.post(
    "/users/{user_id}/transfer/",
    tags=["balances"],
)
async def transfer_money(
        user_id: int,
        transfer: schemas.TransferMoney,
):
    # fixme check user != other
    # fixme check user and other exist
    async with engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
        async with conn.begin():
            balance_query = select(
                [func.sum(transactions.c.amount).label('balance')]
            ).where(
                transactions.c.owner == user_id,
            )
            p(balance_query)
            res = await conn.execute(balance_query)

            transaction_balance = res.scalar() or 0
            print(transaction_balance)

            # transfer_id = str(uuid.uuid4())
            #
            # query = transactions.insert().values(
            #     owner=user_id,
            #     other=transfer.other_id,
            #     amount=(-1 * transfer.amount),
            #     uuid=transfer_id,
            #     created=datetime.datetime.utcnow(),
            # )
            # connection.execute(query)
            #
            # query = transactions.insert().values(
            #     owner=transfer.other_id,
            #     other=user_id,
            #     amount=transfer.amount,
            #     uuid=transfer_id,
            #     created=datetime.datetime.utcnow(),
            # )
            # connection.execute(query)


@router.get("/users/{user_id}/balance/", tags=["balances"], response_model=schemas.User)
async def get_user(user_id: int):
    pass


@router.get("/balances2/", tags=["balances"])
async def get_balances(i: int):
    # async with db.transaction(isolation_level="SERIALIZABLE") as c:
    #     print(c)

    with engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
        # with engine.connect().execution_options(isolation_level="READ COMMITTED") as conn:
        with conn.begin():
            # q = balances.select()
            # print(q)
            # r = await db.fetch_all(q)
            if i == 2:
                c = conn.execute(f'select count(1) from balances')  # where "user"={i}')
                scalar = c.scalar()
                print(f'{i}:', scalar)

                await asyncio.sleep(5)
            if i == 2 and scalar < 15:
                ins = conn.execute(f'insert into balances ("user", amount) values (5, 10)')
            else:
                ins = conn.execute(f'insert into balances ("user", amount) values (5, 10)')

            # print(ins)
            # c = conn.execute(f'select count(1) from balances')  # where "user"={i}') where "user"={i}')
            # print(f'{i}:', c.scalar())

            # await asyncio.sleep(5)
    return {'i': i}


@router.get("/balances/")
async def get_balances(i: int):
    async with db.transaction(isolation='serializable') as con:
        # if i == 2:
        scalar = await db.execute(f'select count(1) from balances where "user"={i}')
        print(f'{i}:', scalar)
        # print(type(con), con)

        await asyncio.sleep(3)

        # if i == 2:
        print('inserting')
        await db.execute(f'insert into balances ("user", amount) values ({i}, 10)')


@router.post(
    "/users/{user_id}/add_money/",
    tags=["balances"],
)
async def add_money(
        user_id: int,
        addition: schemas.AddMoney,
):
    """"""

    # await db.execute(query)

    async with db.transaction():
        await db.execute(query)

    # with engine.connect() as conn:
    #     with conn.begin():
    #         conn.execute(query)


@router.post("/producer/{id}")
async def kafka_produce(id: int):
    """"""
    print(id)
    topic = 'addition'

    user_id = id
    to_id = 3 - id  # 1 or 2

    # msg = {'user_id': 1, 'to_id': 2, 'amount': 1}
    msg = {'user_id': user_id, 'to_id': to_id, 'amount': 1}

    await aioproducer.send(topic, json.dumps(msg).encode("ascii"))
