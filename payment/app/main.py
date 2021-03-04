from fastapi import FastAPI

from .api.v1 import api_router
from .database import create_tables, db
from .broker.producer import aioproducer, create_topics

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
    await aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


create_tables()
create_topics()

app.include_router(api_router)
