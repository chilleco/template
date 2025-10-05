from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.clients.redis import redis_client
from app.core.config import settings
from app.db.base import Base


@pytest.fixture(scope="session")
def event_loop() -> AsyncIterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
def fake_redis(monkeypatch: pytest.MonkeyPatch):
    client = FakeRedis()

    async def _connect():  # noqa: D401
        return client

    monkeypatch.setattr(redis_client, "connect", _connect)
    return client


@pytest_asyncio.fixture
async def session(tmp_path, fake_redis) -> AsyncIterator[AsyncSession]:
    settings.database_dsn = f"sqlite+aiosqlite:///{tmp_path}/test.db"  # type: ignore[assignment]
    engine = create_async_engine(str(settings.database_dsn), echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as session:
        yield session
    await engine.dispose()
