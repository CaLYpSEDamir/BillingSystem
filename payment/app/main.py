from fastapi import FastAPI

from app.api.v1 import api_router
from app.broker.producer import event_producer
from app.broker.topics import create_topic
from app.database import create_tables, db

app = FastAPI(
    title="Billing System",
)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.on_event("startup")
async def startup_event():
    await event_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await event_producer.stop()


create_tables()
create_topic()

app.include_router(api_router)
