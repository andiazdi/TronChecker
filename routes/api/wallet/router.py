from fastapi import APIRouter
from routes.api.wallet.service import WalletInfoServiceDep
from routes.api.wallet.schemas import WalletAddressSchema, WalletInfoSchema, WalletInDB
from dependencies.pagination import PaginationParamsDep

wallet_router = APIRouter(prefix="/wallet", tags=["wallet"])


@wallet_router.get("/")
async def get_wallets(
    service: WalletInfoServiceDep,
    pagination: PaginationParamsDep,
) -> list[WalletInDB]:
    return await service.get_wallets_info(pagination)

@wallet_router.post("/")
async def get_wallet_info(
    schema: WalletAddressSchema,
    service: WalletInfoServiceDep,
) -> WalletInDB:
    return await service.get_wallet_info(schema)
