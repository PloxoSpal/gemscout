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
    SMS_CODE_TTL_SECONDS: int = 300
    SMS_CODE_MAX_ATTEMPTS: int = 5

    #JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    #RabbitMQ
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    @property
    def RABBITMQ_URL(self):
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{str(self.RABBITMQ_PORT)}/"

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()


