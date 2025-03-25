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


YANDEX_SMTP_CONFIG = YandexSMTPConfig(
    **{field: env.str(field) for field in YandexSMTPConfig.model_fields}
)
# GOOGLE_SMTP_CONFIG = GoogleSMTPConfig(
#     **{field: env.str(field) for field in GoogleSMTPConfig.model_fields}
# )