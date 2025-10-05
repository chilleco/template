"""Redis connection and caching utilities."""
import json
from typing import Any
from datetime import timedelta
from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings


class RedisClient:
    """Async Redis client wrapper with utility methods."""

    def __init__(self) -> None:
        self.pool: ConnectionPool | None = None
        self.client: Redis | None = None

    async def connect(self) -> None:
        """Initialize Redis connection pool."""
        self.pool = ConnectionPool.from_url(
            str(settings.REDIS_URL),
            decode_responses=True,
            max_connections=50,
        )
        self.client = Redis(connection_pool=self.pool)

    async def disconnect(self) -> None:
        """Close Redis connection pool."""
        if self.client:
            await self.client.close()
        if self.pool:
            await self.pool.disconnect()

    async def get(self, key: str) -> Any:
        """
        Get value from Redis.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if not self.client:
            return None

        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: int | timedelta | None = None,
    ) -> bool:
        """
        Set value in Redis.

        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds or timedelta

        Returns:
            Success status
        """
        if not self.client:
            return False

        if not isinstance(value, str):
            value = json.dumps(value)

        return await self.client.set(key, value, ex=expire)  # type: ignore

    async def delete(self, key: str) -> bool:
        """
        Delete key from Redis.

        Args:
            key: Cache key

        Returns:
            Success status
        """
        if not self.client:
            return False

        result = await self.client.delete(key)
        return result > 0

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis.

        Args:
            key: Cache key

        Returns:
            True if exists
        """
        if not self.client:
            return False

        return await self.client.exists(key) > 0

    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration for key.

        Args:
            key: Cache key
            seconds: Expiration in seconds

        Returns:
            Success status
        """
        if not self.client:
            return False

        return await self.client.expire(key, seconds)  # type: ignore

    async def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment key value.

        Args:
            key: Cache key
            amount: Increment amount

        Returns:
            New value
        """
        if not self.client:
            return 0

        return await self.client.incrby(key, amount)  # type: ignore

    async def setex(self, key: str, seconds: int, value: Any) -> bool:
        """
        Set value with expiration.

        Args:
            key: Cache key
            seconds: Expiration in seconds
            value: Value to cache

        Returns:
            Success status
        """
        return await self.set(key, value, expire=seconds)


# Global Redis client instance
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """
    Dependency for getting Redis client.

    Returns:
        RedisClient instance
    """
    return redis_client
