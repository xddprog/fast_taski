from functools import wraps
import logging
from typing import Callable, Any, List
from fastapi import Depends, Request, Response
from dishka import FromDishka
import orjson
from backend.core.clients.redis_client import RedisClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s'))
logger.addHandler(handler)


def _key_builder(request: Request, namespace: str) -> str:
    path_params = ":".join(f"{k}={v}" for k, v in sorted(request.path_params.items()))
    router_prefix = request.url.path.split("/")[3]
    return f"{namespace}:{router_prefix}:{path_params}"

def get(namespace: str, expire: int = 60) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            request: Request,
            redis_client: RedisClient = FromDishka[RedisClient](),
            *args,
            **kwargs,
        ) -> Any:
            cache_key = _key_builder(request, namespace)
            try:
                value = await redis_client.get(cache_key)
                if value:
                    return orjson.loads(value)
            except Exception as e:
                logger.error(f"Error fetching cache: key={cache_key}, error={e}")
            value = await func(request, *args, **kwargs)
            try:
                await redis_client.set(cache_key, orjson.dumps(value), ttl=expire)
            except Exception as e:
                logger.error(f"Error setting cache: key={cache_key}, error={e}")
            return value
        return wrapper
    return decorator

def clear(
    namespaces: List[str] | None = None,
    all: bool = False,
    by_key: bool = False,
    set_after: bool = False,
    expire: int = 60
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            request: Request,
            redis_client: RedisClient = FromDishka[RedisClient](),
            *args,
            **kwargs
        ) -> Any:
            if all:
                try:
                    await redis_client.redis.flushdb()
                except Exception as e:
                    logger.error(f"Error clearing entire cache: {e}")
            elif by_key:
                if not namespaces:
                    raise ValueError("Namespace required for by_key")
                cache_key = _key_builder(request, namespaces[0], *args, **kwargs)
                try:
                    await redis_client.redis.delete(cache_key)
                except Exception as e:
                    logger.warning(f"Error clearing cache: key={cache_key}, error={e}")
            else:
                if not namespaces:
                    raise ValueError("Namespaces required unless all=True")
                for namespace in namespaces:
                    try:
                        keys = await redis_client.redis.keys(f"{namespace}:*")
                        if keys:
                            await redis_client.redis.delete(*keys)
                    except Exception as e:
                        logger.warning(f"Error clearing cache: namespace={namespace}, error={e}")
            
            value = await func(request, *args, **kwargs)
            if set_after:
                if not namespaces:
                    raise ValueError("Namespace required for set_after")
                cache_key = _key_builder(request, namespaces[0], *args, **kwargs)
                try:
                    await redis_client.set(cache_key, orjson.dumps(value), ttl=expire)
                    logger.info(f"Cache set after: key={cache_key}")
                except Exception as e:
                    logger.error(f"Error setting cache after: key={cache_key}, error={e}")
            return value
        return wrapper
    return decorator