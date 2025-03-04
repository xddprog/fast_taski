from functools import wraps
from typing import Any, Callable

from redis import Redis

from backend.infrastructure.config.database_configs import REDIS_CONFIG


class RedisClient:
    def __init__(self) -> None:
        self.redis: Redis = Redis(host=REDIS_CONFIG.REDIS_HOST, port=REDIS_CONFIG.REDIS_PORT)

    async def set_item(self, key: str, value: Any, ttl: int = None) -> None:
        if ttl:
            self.redis.set(key, value, ex=ttl)
        else: 
            self.redis.set(key, value)

    async def get_item(self, key: str) -> Any:
        return self.redis.get(key)

    async def delete_item(self, key: str) -> None:
        self.redis.delete(key)