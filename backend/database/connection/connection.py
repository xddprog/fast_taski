from sqlalchemy import select, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from backend.core.config.database_configs import load_database_config
from backend.database.models.base import Base

class DatabaseConnection:
    def __init__(self):
        self.__config = load_database_config()
        self.__engine = create_async_engine(
            url=(
                "postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            ).format(**self.__config.model_dump()),
            poolclass=NullPool,
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self.__engine)

    async def __call__(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return self
