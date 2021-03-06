import json
from typing import Any, Dict

from app.crud import event as event_crud
from app.database import db
from app.schemas.transactions import EventEnum, TransferMoneyEventSchema


async def prepare_event(event):
    """"""
    try:
        print('Started:', event.offset)
        payload = json.loads(event.value)

        if payload['type'] == EventEnum.addition:
            await add_money(payload=payload)
        elif payload['type'] == EventEnum.transfer:
            await transfer_money(payload=payload)
        else:
            raise Exception(f"Unknown event type: {payload['type']}")

    except Exception as e:
        print(f'Error: {e}', event.topic, event.partition,
              event.offset, event.key, event.value, event.timestamp)
    print('Ended:', event.offset)


async def add_money(payload: Dict[str, Any]):
    """Tolerance for double preparing same data."""

    add_event = TransferMoneyEventSchema(**payload)
    await event_crud.prepare_adding_money_event(
        db=db, event=add_event,
    )


async def transfer_money(payload: Dict[str, Any]):
    transfer_event = TransferMoneyEventSchema(**payload)
    await event_crud.prepare_transfer_money_event(
        db=db, event=transfer_event,
    )
