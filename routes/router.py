from fastapi import APIRouter
from routes.api import api_router

router = APIRouter()
router.include_router(api_router)
