from fastapi import APIRouter
from backend.api.v1.endpoints import auth, users, accounts, transfer

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transfer.router, prefix="/transfer", tags=["transfer"])
