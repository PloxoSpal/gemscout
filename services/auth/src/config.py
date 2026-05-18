from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    #Database
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    #Redis
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()


