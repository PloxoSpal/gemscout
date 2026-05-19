from pydantic_settings import SettingsConfigDict, BaseSettings
from enum import Enum

class Mode(str, Enum):
    PROD = 'PROD'
    DEV = 'DEV'
    TEST = 'TEST'


class Settings(BaseSettings):

    #Mode
    MODE: Mode

    #Database
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    #Redis
    REDIS_HOST: str
    REDIS_PORT: int

    #SMSC
    SMS_LOGIN: str | None
    SMS_PASSWORD: str

    #JWT
    JWT_SECRET_KEY = ...
    JWT_ALGORITHM = ...
    ACCESS_TOKEN_EXPIRE_MINUTES = 120

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()


