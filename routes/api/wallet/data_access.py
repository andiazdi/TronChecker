from typing import Annotated
from dependencies.database import DBSessionDep
from models import WalletInfo
from routes.api.wallet.schemas import WalletInfoSchema, WalletInDB
from sqlalchemy import select
from fastapi import Depends


class WalletInfoDataAccess:
    def __init__(self, db_session: DBSessionDep):
        self.db_session = db_session

    async def add_wallet_info(self, wallet_info: WalletInfoSchema) -> WalletInDB:
        wallet = WalletInfo(
            balance=wallet_info.balance,
            bandwidth=wallet_info.bandwidth,
            energy=wallet_info.energy,
            address=wallet_info.address,
        )
        self.db_session.add(wallet)
        await self.db_session.flush()
        return WalletInDB.model_validate(wallet)

    async def get_wallets_info(self, per_page: int, page: int) -> list[WalletInDB]:
        res = await self.db_session.execute(
            select(WalletInfo).offset(per_page * (page - 1)).limit(per_page)
        )
        wallets_info = res.scalars().all()

        return [WalletInDB.model_validate(i) for i in wallets_info]


WalletInfoDataAccessDep = Annotated[WalletInfoDataAccess, Depends(WalletInfoDataAccess)]
