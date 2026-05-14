import requests
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import logging

logger = logging.getLogger("datahub.air_pollution.extract")

def extract_air_pollution():
    api_key = settings.openweather_api_key
    cities = {
        "Berlin": (52.52, 13.41),
        "Munich": (48.14, 11.58),
        "Frankfurt": (50.11, 8.68)
    }

    # Last 5 days because of API limitations
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=5)
    start_unix = int(start.timestamp())
    end_unix = int(end.timestamp())

    url = "https://api.openweathermap.org/data/2.5/air_pollution/history"

    all_data = []
    for city, (lat, lon) in cities.items():
        params = {"lat": lat, "lon": lon, "start": start_unix, "end": end_unix, "appid": api_key}
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            data = r.json().get("list", [])
            for entry in data:
                entry["city"] = city
                all_data.append(entry)
        else:
            logger.warning("%s: %s - %s", city, r.status_code, r.text[:100])

    logger.info("Extracted %s total air pollution records", len(all_data))
    return all_data
