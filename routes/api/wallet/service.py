from typing import Annotated
import httpx
from fastapi import Depends
from fastapi.exceptions import HTTPException
from tronpy import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound, BadAddress

from dependencies.pagination import PaginationParams
from routes.api.wallet.data_access import WalletInfoDataAccessDep
from routes.api.wallet.schemas import WalletInfoSchema, WalletAddressSchema, WalletInDB

from config import settings

TRON_API_BASE = "https://api.trongrid.io"


class WalletInfoService:
    def __init__(self, data_access: WalletInfoDataAccessDep):
        self.data_access = data_access

    async def get_wallet_info(self, wallet_address: WalletAddressSchema) -> WalletInDB:
        async with AsyncTron(
            provider=AsyncHTTPProvider(api_key=settings.TRONGRID_TOKEN)
        ) as client:
            try:
                balance = await client.get_account_balance(wallet_address.address)
                bandwidth = await client.get_bandwidth(wallet_address.address)
                energy = await client.get_energy(wallet_address.address)
            except BadAddress:
                raise HTTPException(status_code=400, detail="Bad address")
            except AddressNotFound:
                raise HTTPException(status_code=404, detail="Address not found")
            except httpx.ConnectTimeout:
                raise HTTPException(status_code=500, detail="Connection timed out")
        wallet_schema = WalletInfoSchema(
            balance=balance,
            address=wallet_address.address,
            bandwidth=bandwidth,
            energy=energy,
        )
        return await self.data_access.add_wallet_info(wallet_schema)

    async def get_wallets_info(self, pagination: PaginationParams) -> list[WalletInDB]:
        return await self.data_access.get_wallets_info(
            pagination.per_page, pagination.page
        )


WalletInfoServiceDep = Annotated[WalletInfoService, Depends(WalletInfoService)]
