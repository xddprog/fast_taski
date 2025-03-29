from functools import wraps
from typing import Any, Callable

from redis.asyncio.client import Redis

from backend.infrastructure.config.database_configs import REDIS_CONFIG


class RedisClient:
    def __init__(self) -> None:
        self.redis: Redis = Redis(host=REDIS_CONFIG.REDIS_HOST, port=REDIS_CONFIG.REDIS_PORT)

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        if ttl:
            await self.redis.set(key, value, ex=ttl)
        else: 
            await self.redis.set(key, value)

    async def get(self, key: str) -> Any:
        return await self.redis.get(key)

    async def delete_by_key(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_by_prefix(self, prefix: str) -> None:
        keys = await self.redis.keys(prefix)
        if not keys:
            return
        await self.redis.delete(*keys)

    async def reset(self) -> None:
        await self.redis.flushall(asynchronous=True)