from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    #Database
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    #S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    ENDPOINT_URL: str
    REGION_NAME: str
    BUCKET_NAME: str

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()


