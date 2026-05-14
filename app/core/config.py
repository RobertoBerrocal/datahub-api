from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("exchange_rates_interval_minutes", "air_pollution_interval_minutes")
    @classmethod
    def validate_scheduler_interval(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Scheduler interval must be greater than 0")
        return value

settings = Settings()
