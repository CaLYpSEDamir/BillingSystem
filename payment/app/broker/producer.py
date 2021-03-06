import asyncio

from aiokafka import AIOKafkaProducer

from app.schemas.transactions import TransferMoneyEventSchema

CLIENT_ID = 'payment'
KAFKA_INSTANCE = "localhost:9092"
TOPIC = 'addition'
TOPIC_PARTITIONS = 2

loop = asyncio.get_event_loop()


class EventProducer(AIOKafkaProducer):
    """"""

    # async def send_event(self, event: AddMoneyEventSchema):
    #     assert type(event) == AddMoneyEventSchema, 'Event must be AddMoneyEventSchema type.'
    #
    #     await self.send(TOPIC, event.json().encode())

    async def send_event(self, event: TransferMoneyEventSchema):
        assert type(event) == TransferMoneyEventSchema, 'Event must be TransferMoneyEventSchema type.'

        await self.send(TOPIC, event.json().encode())


event_producer = EventProducer(
    loop=loop,
    client_id=CLIENT_ID,
    bootstrap_servers=KAFKA_INSTANCE,
)
