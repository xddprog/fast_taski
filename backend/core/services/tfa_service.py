from datetime import timedelta
import secrets

from backend.core.clients.redis_client import RedisClient
from backend.core.repositories.user_repository import UserRepository
from backend.infrastructure.errors.auth_errors import CodeIsIncorrectOrExpired


class TwoFactorAuthService:
    def __init__(self, repository: UserRepository, redis_client: RedisClient):
        self.repository = repository
        self.redis_client = redis_client

    async def generate_code(self, user: str):
        code = secrets.token_hex(3)
        ttl = timedelta(minutes=10)
        await self.redis_client.set(f"user_verify_code:{user}", code, ttl)
        return code
    
    async def check_code(self, user: str, code: str):
        redis_code = await self.redis_client.get(user)
        if redis_code and redis_code.decode() == code:
            await self.redis_client.delete_by_key(user)
            return True
        raise CodeIsIncorrectOrExpired
    