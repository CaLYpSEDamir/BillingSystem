from fastapi import APIRouter

from app.api.v1.routers import users, balances, transactions

api_router = APIRouter(prefix="/users")
api_router.include_router(users.router, tags=["users"])
api_router.include_router(balances.router, tags=["balances"])
api_router.include_router(transactions.router, tags=["transactions"])
