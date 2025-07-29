import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from dependencies.database import base
from routes.api.wallet.schemas import WalletInfoSchema
from routes.api.wallet.data_access import WalletInfoDataAccess
from models import WalletInfo
from config import settings
import random
from string import ascii_letters

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_TESTS_USER}:"
    f"{settings.POSTGRES_TESTS_PASSWORD}@{settings.POSTGRES_TESTS_HOST}:"
    f"{settings.POSTGRES_TESTS_PORT}/{settings.POSTGRES_TESTS_DB}"
)


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_add_wallet_info(async_session):
    data_access = WalletInfoDataAccess(async_session)
    wallet_address = "".join(random.choices(ascii_letters, k=20))

    wallet_schema = WalletInfoSchema(
        address=wallet_address,
        balance=1000,
        bandwidth=200,
        energy=300,
    )

    saved_wallet = await data_access.add_wallet_info(wallet_schema)
    await data_access.db_session.commit()
    assert saved_wallet.address == wallet_address
    assert saved_wallet.balance == 1000
    assert saved_wallet.bandwidth == 200
    assert saved_wallet.energy == 300

    result = await async_session.execute(
        select(WalletInfo).where(WalletInfo.address == wallet_address)
    )
    db_wallet = result.scalar_one_or_none()
    assert db_wallet is not None
    assert db_wallet.balance == 1000
