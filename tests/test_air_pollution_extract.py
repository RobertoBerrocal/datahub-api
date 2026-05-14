import pytest

from app.etl.air_pollution import extract as module


def test_extract_air_pollution_requires_api_key(monkeypatch):
    monkeypatch.setattr(module.settings, "openweather_api_key", None)

    with pytest.raises(ValueError, match="OPENWEATHER_API_KEY is required"):
        module.extract_air_pollution()
