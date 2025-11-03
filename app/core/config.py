from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DataHub API"
    database_url: str = "sqlite:///./datahub.db"
    exchange_rate_api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
