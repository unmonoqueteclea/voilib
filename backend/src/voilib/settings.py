# Copyright (c) 2022-2023 Pablo González Carrizo (unmonoqueteclea)
# All rights reserved.

"""App configuration values.

Settings class will try to obtain, from environment variables, the
value for each configuration parameter, using the default value
defined in the class if a specific value is not found.

If you are running everything through the provided Docker and Docker
Compose configuration, all the needed parameters are provided as
environment variables.

"""
import enum
import pathlib

import pydantic
import redis  # type: ignore
from rq import Queue  # type: ignore

CODE_DIR = pathlib.Path(__file__).parent
BACKEND_DIR = CODE_DIR.parent.parent
REPO_DIR = BACKEND_DIR.parent
REDIS_CACHE_DB_NUMBER = 1


class Environment(enum.Enum):
    test = "test"
    development = "development"
    production = "production"


class Settings(pydantic.BaseSettings):
    environment: str = Environment.development.value
    code_dir: pydantic.DirectoryPath = CODE_DIR
    repo_dir: pydantic.DirectoryPath = REPO_DIR
    media_folder_name: str = "media"
    redis_host: str = "redis"
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    # this user, after its creation, will be automatically assigned
    # admin privileges
    admin_username: str = "voilib-admin"
    # you can generate it with: openssl rand -hex 32
    secret_key: str = ""

    @property
    def data_dir(self) -> pathlib.Path:
        if self.environment == Environment.production.value:
            return pathlib.Path("/data")
        elif self.environment == Environment.test.value:
            return self.repo_dir / "data-test"
        return self.repo_dir / "data"

    @property
    def media_folder(self) -> pathlib.Path:
        return self.data_dir / self.media_folder_name

    @property
    def qdrant_use_file(self) -> bool:
        return self.environment == Environment.test.value

    @property
    def redis_cache(self) -> redis.Redis:
        return redis.Redis(host=self.redis_host, db=REDIS_CACHE_DB_NUMBER)


def create_queue(settings: Settings) -> Queue:
    """Return the main app rq queue"""
    redis_conn = redis.Redis(settings.redis_host)
    return Queue(connection=redis_conn)


settings = Settings()
queue = create_queue(settings)
settings.data_dir.mkdir(exist_ok=True)
