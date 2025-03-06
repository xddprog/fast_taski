from typing import Any, Awaitable, Callable

from pydantic import BaseModel


class BaseTask:
    def __init__(
        self, 
        func: Callable[..., Awaitable[Any]], 
        namespace: str,
        task_name: str,
        func_args: list[Any] | None = None,
        func_kwargs: dict[str, Any] | None = None
    ):
        self.func = func
        self.namespace = namespace
        self.task_name = task_name
        self.full_name = f"{namespace}.{task_name}"
        self.func_args = func_args
        self.func_kwargs = func_kwargs


class RepeatableTask(BaseTask):
    def __init__(
        self, 
        func: Callable[..., Awaitable[Any]], 
        namespace: str,
        task_name: str,
        interval: int | None = None,
        hours: int | None = None,
        minutes: int | None = None,
        max_repeat: int | None = 3
    ):
        super().__init__(func, namespace, task_name)
        
        if not interval and not (hours or minutes):
            raise ValueError("Either interval or hours and minutes must be provided")
        
        self.interval = interval
        self.hours = hours
        self.minutes = minutes
        self.max_repeat = max_repeat
        self._repeat_count = 0 if max_repeat else None
        
    def to_dict(self):
        return {
            "task_name": self.full_name,
            "interval": self.interval,
            "hours": self.hours,
            "minutes": self.minutes,
            "max_repeat": self.max_repeat,
            "repeat_count": self._repeat_count
        }