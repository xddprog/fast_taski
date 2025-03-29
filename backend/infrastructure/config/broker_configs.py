from environs import env
from pydantic import BaseModel


class RabbitMQConfig(BaseModel):
    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_HOST: str
    RABBIT_PORT: int


RABBIT_CONFIG = RabbitMQConfig(**{field: env.str(field) for field in RabbitMQConfig.model_fields})