"""Redis client factory leveraging asyncio support."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis.asyncio import Redis

from app.core.config import settings


class RedisClient:
    def __init__(self) -> None:
        self._redis: Redis | None = None

    async def connect(self) -> Redis:
        if self._redis is None:
            self._redis = Redis.from_url(str(settings.redis_url), encoding="utf-8", decode_responses=True)
        return self._redis

    async def close(self) -> None:
        if self._redis is not None:
            await self._redis.close()
            self._redis = None

    @asynccontextmanager
    async def scoped(self) -> AsyncIterator[Redis]:
        client = await self.connect()
        try:
            yield client
        finally:
            pass


redis_client = RedisClient()


async def get_redis() -> Redis:
    return await redis_client.connect()
