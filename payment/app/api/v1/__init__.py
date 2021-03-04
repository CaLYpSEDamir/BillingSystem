from fastapi import APIRouter

from app.api.v1.routers import users, balances, transactions

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(balances.router, prefix="/balances", tags=["balances"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
