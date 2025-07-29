from fastapi import APIRouter
from routes.api.wallet import wallet_router

api_router = APIRouter(prefix="/api", tags=["api"])
api_router.include_router(wallet_router)
