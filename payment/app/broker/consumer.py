import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import asyncio

from aiokafka import AIOKafkaConsumer

from app.broker.operations import prepare_event
from app.broker.topics import create_topic
from app.database import db
from app.settings import broker_config

create_topic()
loop = asyncio.get_event_loop()


async def consume():
    """Reading events and updating user balances"""
    await db.connect()

    consumer = AIOKafkaConsumer(
        broker_config.topic_name,
        loop=loop,
        bootstrap_servers=f'{broker_config.broker_host}:{broker_config.broker_port}',
        group_id=broker_config.consumer_group_id,
    )
    await consumer.start()

    try:
        async for event in consumer:
            loop.create_task(prepare_event(event=event))
    finally:
        await consumer.stop()
        await db.disconnect()


print(f'Starting consuming messages from `{broker_config.topic_name}` topic.')
loop.run_until_complete(consume())
