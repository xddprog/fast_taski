from environs import Env
from pydantic import BaseModel


env = Env()
env.read_env()


class YandexSMTPConfig(BaseModel):
    YANDEX_SMTP_HOST: str
    YANDEX_SMTP_PORT: int
    YANDEX_SMTP_USER: str
    YANDEX_SMTP_PASSWORD: str


class GoogleSMTPConfig(BaseModel):
    GOOGLE_SMTP_HOST: str
    GOOGLE_SMTP_PORT: int
    GOOGLE_SMTP_USER: str
    GOOGLE_SMTP_PASSWORD: str


def load_yandex_smtp_config() -> YandexSMTPConfig:
    return YandexSMTPConfig(
        YANDEX_SMTP_HOST=env.str("YANDEX_SMTP_HOST"),
        YANDEX_SMTP_PORT=env.int("YANDEX_SMTP_PORT"),
        YANDEX_SMTP_USER=env.str("YANDEX_SMTP_USER"),
        YANDEX_SMTP_PASSWORD=env.str("YANDEX_SMTP_PASSWORD"),
    )


def load_google_smtp_config() -> GoogleSMTPConfig:
    return GoogleSMTPConfig(
        GOOGLE_SMTP_HOST=env.str("GOOGLE_SMTP_HOST"),
        GOOGLE_SMTP_PORT=env.int("GOOGLE_SMTP_PORT"),
        GOOGLE_SMTP_USER=env.str("GOOGLE_SMTP_USER"),
        GOOGLE_SMTP_PASSWORD=env.str("GOOGLE_SMTP_PASSWORD"),
    )
