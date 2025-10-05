"""Database session and engine management."""

from __future__ import annotations

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

_engine: AsyncEngine | None = None
_session_maker: async_sessionmaker[AsyncSession] | None = None


async def init_engine(dsn: str) -> None:
    global _engine, _session_maker
    if _engine is not None:
        return
    _engine = create_async_engine(dsn, echo=False, future=True)
    _session_maker = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    if _session_maker is None:
        raise RuntimeError("Database engine has not been initialized")
    async with _session_maker() as session:
        yield session


async def close_engine() -> None:
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
