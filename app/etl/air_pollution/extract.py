import requests
from app.core.config import settings

BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"

def extract_air_pollution(lat: float, lon: float, start: int, end: int):
    params = {
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end,
        "appid": settings.openweather_api_key
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
