import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import asyncio

from aiokafka import AIOKafkaConsumer

from app.broker.operations import prepare_event
from app.broker.topics import create_topic, get_topic_name
from app.database import db

# FIXME here call topic creation
# FIXME or make it with docker command


topic = get_topic_name()
create_topic()
loop = asyncio.get_event_loop()


async def consume():
    """Reading events and updating user balances"""
    await db.connect()

    consumer = AIOKafkaConsumer(
        topic,
        loop=loop,
        # bootstrap_servers='localhost:9092',
        bootstrap_servers='kafka:9092',
        group_id="addition-consumer",
    )
    await consumer.start()

    try:
        async for event in consumer:
            loop.create_task(prepare_event(event=event))
    finally:
        await consumer.stop()
        await db.disconnect()

print(f'Starting consuming messages from `{topic}` topic.')
loop.run_until_complete(consume())
