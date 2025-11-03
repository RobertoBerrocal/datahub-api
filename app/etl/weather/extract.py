import requests
from app.core.config import settings

def extract_weather_data():
    api_key = settings.openweather_api_key
    city = settings.openweather_city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {response.status_code}")
    return response.json()
