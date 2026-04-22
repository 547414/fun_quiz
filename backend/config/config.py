import os

import toml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = toml.load(fr'{path}/app_config.toml')
active = config.get('settings', {}).get('active', 'development')
env_file = fr'{path}/config/.env.{active}'

load_dotenv(dotenv_path=env_file)


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    MINIO_ENDPOINT: str = os.getenv('MINIO_ENDPOINT')
    MINIO_DEFAULT_BUCKET_PATH: str = os.getenv('MINIO_DEFAULT_BUCKET_PATH')
    MINIO_DEFAULT_BUCKET_NAME: str = os.getenv('MINIO_DEFAULT_BUCKET_NAME')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY')
    MINIO_SECURE: bool = os.getenv('MINIO_SECURE')

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = os.getenv('REDIS_PORT')
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')
    REDIS_DB: int = os.getenv('REDIS_DB')
