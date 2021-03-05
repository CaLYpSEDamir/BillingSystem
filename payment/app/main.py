from fastapi import FastAPI

from .api.v1 import api_router
from .database import create_tables, db
from .broker import create_topics
from .broker.producer import event_producer

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
create_topics()

app.include_router(api_router)
