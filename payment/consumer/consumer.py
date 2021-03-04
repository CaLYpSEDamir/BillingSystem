import asyncio
import json
from aiokafka import AIOKafkaConsumer


# import sys
# from pathlib import Path
# path = Path(__file__)
# sys.path.append(str(path.parent.parent))
# print(sys.path)
# from app.database import engine

# FIXME wait for topic creation
# FIXME or make it with docker command


import sqlalchemy
import databases

DATABASE_URL = 'postgresql://payment:payment@localhost:5432/payment'
engine = sqlalchemy.create_engine(DATABASE_URL)
db = databases.Database(
    DATABASE_URL,
    min_size=5,
    max_size=10,
)


topic = 'addition'

loop = asyncio.get_event_loop()


async def activate_db():
    await db.connect()

# asyncio.run(activate())


async def add_money(user_id, amount):
    async with db.transaction():
        query = f'UPDATE balances SET amount = amount+{amount} WHERE "user" = {user_id};'
        await db.execute(query)


async def transfer_money(from_id: int, to_id: int, amount: float, offset: int):
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

    await activate_db()

    consumer = AIOKafkaConsumer(
        topic,
        loop=loop,
        bootstrap_servers='localhost:9092',
        group_id="addition-consumer",
        heartbeat_interval_ms=2000,
    )
    await consumer.start()

    try:
        async for msg in consumer:
            print('Consumed:', msg.offset)
            # print("consumed: ", msg.topic, msg.partition, msg.offset,
            #       msg.key, msg.value, msg.timestamp)

            data = json.loads(msg.value)
            print(1)
            # await add_money(user_id=data['user_id'], amount=data['amount'], offset=msg.offset)
            # await transfer_money(
            #     from_id=data['user_id'],
            #     to_id=data['to_id'],
            #     amount=data['amount'],
            #     offset=msg.offset,
            # )

            loop.create_task(transfer_money(
                from_id=data['user_id'],
                to_id=data['to_id'],
                amount=data['amount'],
                offset=msg.offset,
            ))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
        await db.disconnect()


loop.run_until_complete(consume())
