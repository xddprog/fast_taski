from typing import AsyncIterable
from dishka import FromDishka, Provider, Scope, provide
from dishka.integrations.fastapi import inject
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core import clients, repositories, services
from backend.core.dto.user_dto import BaseUserModel
from backend.core.tasks_manager.manager import TasksManager
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection
from backend.utils.auth_requests import AuthRequests


class RequestProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self, db_connection: DatabaseConnection) -> AsyncIterable[AsyncSession]:
        session = await db_connection.get_session()
        try:
            yield session
        finally:
            await session.close()

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, session: AsyncSession) -> services.AuthService:
        return services.AuthService(repository=repositories.UserRepository(session=session))

    @provide(scope=Scope.REQUEST)
    def get_tfa_service(self, session: AsyncSession, redis_client: clients.RedisClient) -> services.TwoFactorAuthService:
        return services.TwoFactorAuthService(
            repository=repositories.UserRepository(session=session),
            redis_client=redis_client
        )
    
    @provide(scope=Scope.REQUEST)
    def get_note_service(self, session: AsyncSession) -> services.NoteService:    
        return services.NoteService(repository=repositories.NoteRepository(session=session))
    
    @provide(scope=Scope.REQUEST)
    def get_task_service(self, session: AsyncSession) -> services.TaskService:    
        return services.TaskService(repository=repositories.TaskRepository(session=session))
    
    @provide(scope=Scope.REQUEST)
    def get_team_service(
        self, 
        session: AsyncSession, 
        tasks_manager: TasksManager, 
        redis_client: clients.RedisClient,
        aws_client: clients.AWSClient
    ) -> services.TeamService:    
        return services.TeamService(
            repository=repositories.TeamRepository(session=session),
            smtp_clients=clients.SMTPClients(),
            redis_client=redis_client,
            tasks_manager=tasks_manager,
            aws_client=aws_client
        )
    
    @provide(scope=Scope.REQUEST)
    def get_user_service(
        self, 
        session: AsyncSession, 
        tasks_manager: TasksManager,
        aws_client: clients.AWSClient
    ) -> services.UserService:    
        return services.UserService(
            repository=repositories.UserRepository(session=session),
            aws_client=aws_client,
            tasks_manager=tasks_manager
        )
    
    @provide(scope=Scope.REQUEST)
    def get_tag_service(self, session: AsyncSession) -> services.TagService:    
        return services.TagService(repository=repositories.TagRepository(session=session))
    
    @provide(scope=Scope.REQUEST)
    def get_column_service(self, session: AsyncSession) -> services.ColumnService:    
        return services.ColumnService(repository=repositories.ColumnRepository(session=session))
    
    @provide(scope=Scope.REQUEST)
    async def get_auth_requests(self) -> AuthRequests:
        return AuthRequests()

@inject
async def get_current_user_dependency(
    auth_service: FromDishka[services.AuthService], 
    request: Request
) -> BaseUserModel:
    token = request.cookies.get('access_token')
    data = await auth_service.verify_token(token)
    return await auth_service.check_user_exist(data)
