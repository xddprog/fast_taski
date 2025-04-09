from typing import Any
from pydantic import BaseModel
from sqlalchemy.orm import MappedColumn
from backend.core.clients.aws_client import AWSClient
from backend.core.clients.redis_client import RedisClient
from backend.core.clients.smtp_clients import SMTPClients
from backend.core.repositories.base import SqlAlchemyRepository
from backend.core.tasks_manager.manager import TasksManager
from backend.infrastructure.interfaces.repository import RepositoryInterface


class BaseDbModelService[ModelType]:
    def __init__(
        self, repository: RepositoryInterface[ModelType],
        tasks_manager: TasksManager = None,
        aws_client: AWSClient = None,
        redis_client: RedisClient = None,
        smtp_clients: SMTPClients = None
    ):
        self.repository = repository
        self.tasks_manager = tasks_manager
        self.aws_client = aws_client
        self.redis_client = redis_client
        self.smtp_clients = smtp_clients
    