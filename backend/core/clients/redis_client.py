from functools import wraps
from typing import Any, Callable

from redis import Redis

from backend.core.config.database_configs import load_redis_config


class RedisClient:
    def __init__(self) -> None:
        self.config = load_redis_config()
        self.redis: Redis = Redis(host=self.config.REDIS_HOST, port=self.config.REDIS_PORT)
        # self.redis.flushdb()

    async def set_item(self, key: str, value: Any, ttl: int = None) -> None:
        if ttl:
            self.redis.set(key, value, ex=ttl)
        else: 
            self.redis.set(key, value)

    async def get_item(self, key: str) -> Any:
        return self.redis.get(key)

    async def delete_item(self, key: str) -> None:
        self.redis.delete(key)