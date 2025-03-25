from environs import Env
from pydantic import BaseModel


env = Env()
env.read_env()


class JwtConfig(BaseModel):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_TIME: int
    JWT_REFRESH_TOKEN_TIME: int


class VKOAuthConfig(BaseModel):
    VK_BASE_URL: str
    VK_API_URL: str
    VK_CLIENT_ID: str
    VK_CLIENT_SECRET: str


class YandexOAuthConfig(BaseModel):
    YANDEX_BASE_URL: str
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_API_URL: str



JWT_CONFIG = JwtConfig(
    **{field: env.str(field) for field in JwtConfig.model_fields}
)
VK_CONFIG = VKOAuthConfig(
    **{field: env.str(field) for field in VKOAuthConfig.model_fields}   
)
YANDEX_CONFIG = YandexOAuthConfig(
    **{field: env.str(field) for field in YandexOAuthConfig.model_fields}
)
