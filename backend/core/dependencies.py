from typing import Annotated, AsyncGenerator
from urllib import request

from fastapi import Cookie, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession  

from backend.core.clients.redis_client import RedisClient
from backend.core.clients.smtp_clients import SMTPClients
import backend.services as services
import backend.repositories as repositories
from backend.dto.user_dto import BaseUserModel
from backend.services import AuthService


async def get_redis_client(request: Request) -> RedisClient:
    return request.app.state.redis_client


async def get_smtp_clients(request: Request) -> SMTPClients:
    return request.app.smtp_clients

async def get_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    session = await request.app.state.db_connection.get_session()
    try:
        yield session
    finally:
        await session.close()


async def get_auth_service(session=Depends(get_session)):
    return services.AuthService(
        repository=repositories.UserRepository(
            session=session
        )
    )


async def get_current_user_dependency(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request
):
    token = request.cookies.get('access_token')
    data = await auth_service.verify_token(token)
    return await auth_service.check_user_exist(data)


async def get_user_service(session=Depends(get_session)):
    return services.UserService(
        repository=repositories.UserRepository(
            session=session
        )
    )


async def get_tfa_service(    
    session=Depends(get_session),
    redis_client=Depends(get_redis_client)
):
    return services.TwoFactorAuthService(
        repository=repositories.UserRepository(
            session=session,
        ),
        redis_client=redis_client
    )
