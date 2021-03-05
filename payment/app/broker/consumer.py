import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import asyncio
import json
from typing import Any, Dict

import sqlalchemy
import databases
from aiokafka import AIOKafkaConsumer

from app.models import (
    users as users_model,
    transactions as trans_model,
)
from app.schemas.transactions import (
    AddMoneyEventSchema, EventEnum,
)

# from app.database import engine, db

# FIXME wait for topic creation
# FIXME or make it with docker command


DATABASE_URL = 'postgresql://payment:payment@localhost:5432/payment'
engine = sqlalchemy.create_engine(DATABASE_URL)
db = databases.Database(
    DATABASE_URL,
    min_size=5,
    max_size=10,
)

topic = 'addition'
loop = asyncio.get_event_loop()


async def prepare_event(event):
    """"""
    print('Started:', event.offset)
    payload = json.loads(event.value)
    if payload['type'] == EventEnum.addition:
        await add_money(payload=payload)
    elif payload['type'] == EventEnum.transfer:
        await transfer_money(payload=payload)

    print('Ended:', event.offset)


async def add_money(payload: Dict[str, Any]):
    addition = AddMoneyEventSchema(**payload)
    print(addition)
    trans_id = addition.transaction_id
    owner = addition.owner
    amount = addition.amount

    async with db.transaction():

        query = f'UPDATE balances SET amount = amount+{amount} WHERE owner = {owner};'
        await db.execute(query)


async def transfer_money(payload: Dict[str, Any]):
    async with db.transaction():
        print('Started:', offset)
        substract_query = f'UPDATE balances SET amount = amount+{amount} WHERE "user" = {from_id};'
        addition_query = f'UPDATE balances SET amount = amount+{amount} WHERE "user" = {to_id};'

        min_ = min(from_id, to_id)
        if from_id == min_:
            first = substract_query
            second = addition_query
        else:
            first = addition_query
            second = substract_query

        try:
            await db.execute(first)
            await db.execute(second)
        except Exception as e:
            print(f"Error: {e}")
            raise e

        # try:
        #     query = f'UPDATE balances SET amount = amount+{amount} WHERE "user" = {from_id};'
        #     await db.execute(query)
        #     # sl_q = 'select pg_sleep(0.5);'
        #     # await db.execute(sl_q)
        #     # raise
        #     query = f'UPDATE balances SET amount = amount-{amount} WHERE "user" = {to_id};'
        #     await db.execute(query)
        #
        # except Exception as e:
        #     print(f"Error: {e}")
        #     raise e

        print('Ended:', offset)


async def consume():
    """"""
    await db.connect()

    consumer = AIOKafkaConsumer(
        topic,
        loop=loop,
        bootstrap_servers='localhost:9092',
        group_id="addition-consumer",
        # heartbeat_interval_ms=2000,
    )
    await consumer.start()

    try:
        async for event in consumer:
            print('Consumed:', event.offset)
            # print("consumed: ", msg.topic, msg.partition, msg.offset,
            #       msg.key, msg.value, msg.timestamp)

            loop.create_task(prepare_event(event=event))

            # loop.create_task(transfer_money(
            #     from_id=data['user_id'],
            #     to_id=data['to_id'],
            #     amount=data['amount'],
            #     offset=msg.offset,
            # ))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
        await db.disconnect()


loop.run_until_complete(consume())
