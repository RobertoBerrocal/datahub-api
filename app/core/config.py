from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base
    app_name: str = "DataHub API"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///datahub.db"

    # Exchange Rates API
    exchange_rate_api_key: str | None = None

    # OpenWeather API
    openweather_api_key: str | None = None
    openweather_city: str = "Berlin"

    class Config:
        env_file = ".env"

settings = Settings()
