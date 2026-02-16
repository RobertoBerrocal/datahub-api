from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base
    app_name: str = "DataHub API"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./data/datahub.db"

    # Exchange Rates API
    exchange_rate_api_key: str | None = None

    # OpenWeather API
    openweather_api_key: str | None = None
    openweather_city: str = "Berlin"

    # Scheduler
    scheduler_enabled: bool = False
    timezone: str = "Europe/Berlin"
    exchange_rates_interval_minutes: int = 1440  # daily
    air_pollution_interval_minutes: int = 60     # hourly

    class Config:
        env_file = ".env"

settings = Settings()
