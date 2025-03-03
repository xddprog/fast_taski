from environs import Env
from pydantic import BaseModel


env = Env()
env.read_env()


class JwtConfig(BaseModel):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_TIME: int
    JWT_REFRESH_TOKEN_TIME: int



class GithubOAuthConfig(BaseModel):
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_BASE_URL: str
    GITHUB_API_URL: str


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


def load_jwt_config() -> JwtConfig:
    return JwtConfig(
        JWT_SECRET=env.str("JWT_SECRET"),
        JWT_ALGORITHM=env.str("JWT_ALGORITHM"),
        JWT_ACCESS_TOKEN_TIME=env.int("JWT_ACCESS_TOKEN_TIME"),
        JWT_REFRESH_TOKEN_TIME=env.int("JWT_REFRESH_TOKEN_TIME")
    )



def load_github_config() -> GithubOAuthConfig:
    return GithubOAuthConfig(
        GITHUB_CLIENT_ID=env.str("GITHUB_CLIENT_ID"),
        GITHUB_CLIENT_SECRET=env.str("GITHUB_CLIENT_SECRET"),
        GITHUB_BASE_URL=env.str("GITHUB_BASE_URL"),
        GITHUB_API_URL=env.str("GITHUB_API_URL"),
    )


def load_vk_config() -> VKOAuthConfig:
    return VKOAuthConfig(
        VK_BASE_URL=env.str("VK_BASE_URL"),
        VK_API_URL=env.str("VK_API_URL"),
        VK_CLIENT_ID=env.str("VK_CLIENT_ID"),
        VK_CLIENT_SECRET=env.str("VK_CLIENT_SECRET"),
    )


def load_yandex_config() -> YandexOAuthConfig:
    return YandexOAuthConfig(
        YANDEX_BASE_URL=env.str("YANDEX_BASE_URL"),
        YANDEX_CLIENT_ID=env.str("YANDEX_CLIENT_ID"),
        YANDEX_CLIENT_SECRET=env.str("YANDEX_CLIENT_SECRET"),
        YANDEX_API_URL=env.str("YANDEX_API_URL"),
    )