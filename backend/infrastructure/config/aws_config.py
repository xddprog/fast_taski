from environs import Env, env
from pydantic import BaseModel


env = Env()
env.read_env()



class AWSStorageConfig(BaseModel):
    AWS_BUCKET_NAME: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_ENDPOINT_URL: str


AWS_STORAGE_CONFIG = AWSStorageConfig(
    **{field: env.str(field) for field in AWSStorageConfig.model_fields}
)