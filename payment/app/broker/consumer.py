import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import asyncio

from aiokafka import AIOKafkaConsumer

from app.broker.operations import prepare_event
from app.database import db

# FIXME here call topic creation
# FIXME or make it with docker command


# DATABASE_URL = 'postgresql://payment:payment@localhost:5432/payment'
# engine = sqlalchemy.create_engine(DATABASE_URL)
# db = databases.Database(
#     DATABASE_URL,
#     min_size=5,
#     max_size=10,
# )

topic = 'addition'
loop = asyncio.get_event_loop()


async def consume():
    """"""
    await db.connect()

    consumer = AIOKafkaConsumer(
        topic,
        loop=loop,
        bootstrap_servers='localhost:9092',
        group_id="addition-consumer",
    )
    await consumer.start()

    try:
        async for event in consumer:
            print('Consumed:', event.offset)
            # print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            loop.create_task(prepare_event(event=event))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
        await db.disconnect()


loop.run_until_complete(consume())
