import os

from src.samples.singletone import Singletone
from src.config import DEBUG


class EnvContainer(Singletone): # Посмотреть Pydantic settings
    def _init(self) -> None:
        super().__init__()

        self.__key_api: str = "KEY_API"

        self.__postgresql_db_name: str = "POSTGRESQL_DB_NAME"
        self.__postgresql_user_name: str = "POSTGRESQL_USER"
        self.__postgresql_password: str = "POSTGRESQL_PASSWORD"
        self.__postgresql_host: str = "POSTGRESQL_HOST"
        self.__postgresql_port: str = "POSTGRESQL_PORT"

        self.__minio_url: str = 'MINIO_BACK_URL'
        self.__minio_access_key: str = 'MINIO_ACCESS_KEY'
        self.__minio_secret_key: str = 'MINIO_SECRET_KEY'
        self.__minio_bucket: str = 'MINIO_BUCKET'

        self.__debug_env: dict = {}
        if DEBUG:
            self.__debug_env: dict = {
                "KEY_API": "xxxxxxxxxxxxxxxxxxx",

                "POSTGRESQL_DB_NAME": "NewsApi",
                "POSTGRESQL_USER": "postgres",
                "POSTGRESQL_PASSWORD": "nikol",
                "POSTGRESQL_HOST": "127.0.0.1",
                "POSTGRESQL_PORT": 5432,

                'MINIO_BACK_URL': '127.0.0.1:9000',
                'MINIO_ACCESS_KEY': 'minioadmin',
                'MINIO_SECRET_KEY': 'minioadmin',
                'MINIO_BUCKET': 'cameras',
            }

    def __get_from_env(self, key):
        return self.__debug_env[key] if DEBUG else os.environ[key]

    @property
    def key_api(self):
        return self.__get_from_env(self.__key_api)

    @property
    def postgresql_db_name(self):
        return self.__get_from_env(self.__postgresql_db_name)

    @property
    def postgresql_user_name(self):
        return self.__get_from_env(self.__postgresql_user_name)

    @property
    def postgresql_password(self):
        return self.__get_from_env(self.__postgresql_password)

    @property
    def postgresql_host(self):
        return self.__get_from_env(self.__postgresql_host)

    @property
    def postgresql_port(self):
        return int(self.__get_from_env(self.__postgresql_port))

    @property
    def minio_url(self):
        return self.__get_from_env(self.__minio_url)

    @property
    def minio_access_key(self):
        return self.__get_from_env(self.__minio_access_key)

    @property
    def minio_secret_key(self):
        return self.__get_from_env(self.__minio_secret_key)

    @property
    def minio_client_settings(self):
        return {
            'endpoint': self.minio_url,
            'access_key': self.minio_access_key,
            'secret_key': self.minio_secret_key,
            'secure': False,
        }

    @property
    def minio_bucket(self):
        return self.__get_from_env(self.__minio_bucket)


env_container = EnvContainer()

__all__ = [env_container]
