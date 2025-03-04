from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from backend.infrastructure.config.database_configs import DB_CONFIG
from backend.infrastructure.database.models.base import Base

class DatabaseConnection:
    def __init__(self):
        self.__engine = create_async_engine(
            url=DB_CONFIG.get_postgres_url(),
            poolclass=NullPool,
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self.__engine)

    async def __call__(self):
        print(1)
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return self
