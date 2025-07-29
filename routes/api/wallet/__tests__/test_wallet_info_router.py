import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app

@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_engine):
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.mark.asyncio
async def test_wallet_info_router():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/api"
    ) as client:
        response = await client.post(
            "/wallet/", json={"address": "TNbJH9aCrFgdHP7dqTD5MyXxZYhNWapBgi"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "balance" in data
        assert "bandwidth" in data
        assert "energy" in data
        assert "address" in data
