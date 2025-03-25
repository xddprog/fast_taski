import asyncio
from datetime import timedelta
import threading
import time
from typing import Any, Awaitable, Callable

import orjson
from backend.core.clients.rabbit_client import RabbitClient
from backend.core.tasks_manager.tasks import BaseTask, RepeatableTask


class SingletonMeta(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__()
        return cls._instances[cls]
    

class TasksManager(metaclass=SingletonMeta):
    def __init__(self):
        self._rabbit = RabbitClient()
        self._repeatable_tasks: dict[str, RepeatableTask] = {}
        self._default_tasks: dict[str, BaseTask] = {}
        self._queue = None
        self._delayed_queue = None
        self._running = False

    async def add_base_task(
        self, 
        func: Callable[..., Awaitable[Any]], 
        namespace: str, 
        task_name: str,
        func_args: list[Any] | None = None,
        func_kwargs: dict[str, Any] | None = None
    ) -> None:
        new_task = BaseTask(func, namespace, task_name, func_args, func_kwargs)
        self._default_tasks[new_task.full_name] = new_task
        await self._rabbit.send_message(self._queue.name, {"task_name": new_task.full_name})

    async def add_repeatable_task(
        self,
        func: Callable[..., Awaitable[Any]], 
        namespace: str, 
        task_name: str,
        func_args: list[Any] | None = None,
        func_kwargs: dict[str, Any] | None = None,
        interval: int | None = None,
        hours: int | None = None,
        minutes: int | None = None,
        max_repeat: int | None = 3
    ) -> None:
        new_task = RepeatableTask(
            func=func, 
            namespace=namespace, 
            task_name=task_name, 
            func_args=func_args, 
            func_kwargs=func_kwargs, 
            interval=interval, 
            hours=hours, 
            minutes=minutes, 
            max_repeat=max_repeat
        )
        self._repeatable_tasks[new_task.full_name] = new_task
        await self._send_delayed_task(new_task)

    async def _run_repeatable_task(self, task_name: str):
        try:
            task = self._repeatable_tasks.get(task_name)
            if task and task.max_repeat and task._repeat_count <= task.max_repeat:
                await task.func(*(task.func_args or []), **(task.func_kwargs or {}))
                task._repeat_count += 1
                print(task._repeat_count, task.max_repeat)
            if task and task._repeat_count == task.max_repeat:
                self._repeatable_tasks.pop(task_name)
            else:
                await self._send_delayed_task(task)
        except Exception:
            pass
    
    def _calculate_delay(self, task: RepeatableTask) -> int:
        minutes = 60 * (task.hours or 0) + (task.minutes or 0)
        return minutes * 10

    async def _send_delayed_task(self, task: RepeatableTask):
        if task.interval:
            delay = task.interval
        else:
            delay = self._calculate_delay(task)
        if delay > 0:
            await self._rabbit.send_delayed_message(
                self._delayed_queue.name,
                task.to_dict(),
                timedelta(seconds=10)
            )

    async def _run_default_task(self, task_name: str):
        try:
            task = self._default_tasks.get(task_name)
            if task:
                await task.func(*(task.func_args or []), **(task.func_kwargs or {}))
                self._default_tasks.pop(task.full_name)
        except Exception:
            pass

    async def _run_handle_queue(self):
        await self._rabbit.init_connection()

        while not self._queue:
            self._queue = await self._rabbit.declare_queue("tasks_queue")
        
        while not self._delayed_queue:
            self._delayed_queue = await self._rabbit.declare_delayed_queue(
                "delayed_tasks_queue",
                dead_letter_exchange="dlx_exchange",
                dead_letter_routing_key="tasks_queue"
            )

        async with self._queue.iterator() as messages:
            async for message in messages:
                if not self._running:
                    break
                async with message.process():
                    task_data = orjson.loads(message.body)
                    task_name = task_data.get("task_name")
                    if task_name in self._repeatable_tasks:
                        await self._run_repeatable_task(task_name)
                    elif task_name in self._default_tasks:
                        await self._run_default_task(task_name)

    async def start(self):
        self._running = True
        asyncio.create_task(self._run_handle_queue())

    async def close(self):
        self._running = False
        await self._rabbit.delete_queue("tasks_queue")
        await self._rabbit.delete_queue("delayed_tasks_queue")
