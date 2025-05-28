from functools import wraps
import logging
from typing import Callable, Any, List
from fastapi import Depends, Request, Response
from dishka import FromDishka
import orjson
from pydantic import BaseModel
from backend.core.clients.redis_client import RedisClient
from backend.core.dto.user_dto import BaseUserModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s'))
logger.addHandler(handler)


def _key_builder(namespace: str, queries: dict | None = None, user_id: str | None = None) -> str:
    queries = ":".join([f"{k}={v}" for k, v in queries.items()]) 
    return f"{namespace}:{queries}" if user_id is None else f"{namespace}:user_id={user_id}:{queries}"


def get(namespace: str, expire: int = 60, queries: list[str] | None = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            request: Request,
            redis_client: RedisClient = RedisClient(),
            *args,
            **kwargs,
        ) -> Any:
            filter_queries = {k: v for k, v in kwargs.items() if k in queries} if queries else {}
            current_user: BaseUserModel = kwargs.get("current_user") if kwargs.get("current_user") else None
            cache_key = _key_builder(namespace, filter_queries, current_user.id if current_user else None)

            try:
                value = await redis_client.get(cache_key)
                if value:
                    value = orjson.loads(value)
                    return value
            except Exception as e:
                logger.error(f"Error fetching cache: key={cache_key}, error={e}")

            value = await func(request, *args, **kwargs)

            try:
                if isinstance(value, dict):
                    dumped = orjson.dumps(value)
                elif isinstance(value, BaseModel):
                    dumped = orjson.dumps(value.model_dump())
                elif isinstance(value, list):
                    dumped = []
                    for item in value:
                        if isinstance(item, BaseModel):
                            dumped.append(item.model_dump())
                    dumped = orjson.dumps(dumped)

                await redis_client.set(cache_key, dumped, ttl=expire)
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
    expire: int = 60,
    queries: List[str] | dict | None = None,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            request: Request,
            redis_client: RedisClient = RedisClient(),
            *args,
            **kwargs
        ) -> Any:
            value = await func(request, *args, **kwargs)
            current_user: BaseUserModel = kwargs.get("current_user")

            if isinstance(queries, dict):
                filter_queries = {}
                for k, v in queries.items():
                    if v in kwargs:
                        filter_queries[k] = kwargs[v]
            else:
                filter_queries = {k: v for k, v in kwargs.items() if k in queries} if queries else {}

            if all:
                try:
                    await redis_client.reset()
                except Exception as e:
                    logger.error(f"Error clearing entire cache: {e}")

            elif by_key:
                cache_key = None
                try:
                    if not namespaces:
                        raise ValueError("Namespace required for by_key")
                    if isinstance(queries, list):
                        cache_key = _key_builder(namespaces[0], {queries[0]: filter_queries.get(queries[0])}, current_user.id)
                        await redis_client.delete_by_key(cache_key)
                    else:
                        for namespace, query in queries.items():
                            cache_key = _key_builder(namespace, {query: filter_queries.get(query)}, current_user.id)
                            await redis_client.delete_by_key(cache_key)
                except Exception as e:
                    logger.warning(f"Error clearing cache: key={cache_key}, error={e}")

            else:
                if not namespaces:
                    raise ValueError("Namespaces required unless all=True")
                
                for namespace in namespaces:
                    try:
                        await redis_client.delete_by_prefix(f"{namespace}:*")
                    except Exception as e:
                        logger.warning(f"Error clearing cache: namespace={namespace}, error={e}")
                        
            if set_after:
                if not namespaces:
                    raise ValueError("Namespace required for set_after")
                
                if isinstance(queries, list):
                    cache_key = _key_builder(namespaces[0], {queries[0]: filter_queries.get(queries[0])}, current_user.id)
                else:
                    cache_key = _key_builder(namespaces[0], filter_queries, current_user.id)

                try:
                    if isinstance(value, dict):
                        dumped = orjson.dumps(value)
                    elif isinstance(value, BaseModel):
                        dumped = orjson.dumps(value.model_dump())
                    elif isinstance(value, list):
                        dumped = []
                        for item in value:
                            if isinstance(item, BaseModel):
                                dumped.append(item.model_dump())
                        dumped = orjson.dumps(dumped)
        
                    await redis_client.set(cache_key, dumped, ttl=expire)
                    logger.info(f"Cache set after: key={cache_key}")
                except Exception as e:
                    logger.error(f"Error setting cache after: key={cache_key}, error={e}")
            return value
        return wrapper
    return decorator