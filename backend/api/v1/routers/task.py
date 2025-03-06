import asyncio
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request

import backend.core.cache.redis_cache as cache
from backend.core.clients.aws_client import AWSClient
from backend.core.clients.rabbit_client import RabbitClient
from backend.core.clients.redis_client import RedisClient
from backend.core.worker.manager import TaskManager
from backend.core.worker.tasks import BaseTask, RepeatableTask


router = APIRouter()


@router.get("/{task_id}/notes/{zxc}")
@inject
@cache.get(namespace="notes", expire=60)
async def get_notes(request: Request, task_id: int, zxc: str):
    await asyncio.sleep(1)
    return {"detail": "hello"}


@router.delete("/{task_id}/notes/{zxc}")
@inject
async def get_notes(request: Request, task_id: int, zxc: str, aws: FromDishka[AWSClient]):
    t = TaskManager()
    await t.add_repeatable_task(
        RepeatableTask(
            func=aws.get_client, 
            namespace="notes", 
            task_name="test", 
            minutes=1
        )
    )
    await t.add_base_task(
        BaseTask(
            func=aws.get_client, 
            namespace="notes", 
            task_name="test1"
        )
    )
    return {"detail": "hello"}
