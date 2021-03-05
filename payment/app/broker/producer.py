import asyncio
import json
from typing import Any, Dict

from aiokafka import AIOKafkaProducer
from app.schemas.transactions import (
    AddMoneyEventSchema,
    EventEnum,
)

CLIENT_ID = 'payment'
KAFKA_INSTANCE = "localhost:9092"
TOPIC = 'addition'
TOPIC_PARTITIONS = 2

loop = asyncio.get_event_loop()


class EventProducer(AIOKafkaProducer):
    """"""

    async def addition_event(
            self,
            user_id: int,
            amount: float,
            transaction_id: int,
    ):
        event = AddMoneyEventSchema(
            owner=user_id,
            type= EventEnum.addition.value,
            amount=amount,
            transaction_id=transaction_id,
        )

        await self.send(TOPIC, event.json().encode())


event_producer = EventProducer(
    loop=loop,
    client_id=CLIENT_ID,
    bootstrap_servers=KAFKA_INSTANCE,
)
