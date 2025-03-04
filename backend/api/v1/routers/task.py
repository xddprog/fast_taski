import asyncio
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request

import backend.core.cache.redis_cache as cache
from backend.core.clients.redis_client import RedisClient


router = APIRouter()


@router.get("/{task_id}/notes/{zxc}")
@inject
@cache.get(namespace="notes", expire=60)
async def get_notes(request: Request, task_id: int, zxc: str):
    await asyncio.sleep(1)
    return {"detail": "hello"}


@router.delete("/{task_id}/notes/{zxc}")
@inject
@cache.clear(all=True, namespaces=["notes"], expire=60)
async def get_notes(request: Request, task_id: int, zxc: str):
    await asyncio.sleep(1)
    return {"detail": "hello"}
