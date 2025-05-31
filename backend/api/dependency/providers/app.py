import asyncio
from dishka import Provider, Scope, provide
from fastapi import Request

from backend.core.clients.aws_client import AWSClient
from backend.core.clients.rabbit_client import RabbitClient
from backend.core.clients.redis_client import RedisClient
from backend.core.clients.smtp_clients import SMTPClients
from backend.core.tasks_manager.manager import TasksManager
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_redis_client(self) -> RedisClient:
        return RedisClient()

    @provide(scope=Scope.APP)
    async def get_smtp_clients(self, tasks_manager: TasksManager) -> SMTPClients:
        return SMTPClients(tasks_manager)

    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> DatabaseConnection:
        return DatabaseConnection()
    
    @provide(scope=Scope.APP)
    async def get_aws_client(self) -> AWSClient:
        return await AWSClient()()
    
    @provide(scope=Scope.APP)
    async def get_tasks_manager(self) -> TasksManager:
        return TasksManager()
    