import asyncio

from aiokafka import AIOKafkaProducer

from app.schemas.transactions import TransferMoneyEventSchema
from app.settings import broker_config


class EventProducer(AIOKafkaProducer):
    """"""

    async def send_event(self, event: TransferMoneyEventSchema):
        assert type(event) == TransferMoneyEventSchema, 'Event must be TransferMoneyEventSchema type.'

        await self.send(broker_config.topic_name, event.json().encode())


loop = asyncio.get_event_loop()

print(f'{broker_config.broker_host}:{broker_config.broker_port}')

event_producer = EventProducer(
    loop=loop,
    client_id=broker_config.client_id,
    bootstrap_servers=f'{broker_config.broker_host}:{broker_config.broker_port}',
)
