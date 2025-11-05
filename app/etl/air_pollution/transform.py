import pandas as pd
from datetime import datetime

def transform_air_pollution(raw_data: dict, city_id: int):
    records = []
    for entry in raw_data.get("list", []):
        c = entry["components"]
        records.append({
            "city_id": city_id,
            "aqi": entry["main"]["aqi"],
            "co": c["co"],
            "no": c["no"],
            "no2": c["no2"],
            "o3": c["o3"],
            "so2": c["so2"],
            "pm2_5": c["pm2_5"],
            "pm10": c["pm10"],
            "nh3": c["nh3"],
            "timestamp": datetime.utcfromtimestamp(entry["dt"])
        })
    return pd.DataFrame(records)
