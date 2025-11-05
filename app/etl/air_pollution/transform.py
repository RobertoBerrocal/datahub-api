import pandas as pd
from datetime import datetime, timezone

def transform_air_pollution(raw_data):
    if not raw_data:
        print("[WARN] No data to transform.")
        return pd.DataFrame()

    rows = []
    for entry in raw_data:
        comps = entry.get("components", {})
        main = entry.get("main", {})
        rows.append({
            "city": entry["city"],
            "aqi": main.get("aqi"),
            "co": comps.get("co"),
            "no": comps.get("no"),
            "no2": comps.get("no2"),
            "o3": comps.get("o3"),
            "so2": comps.get("so2"),
            "pm2_5": comps.get("pm2_5"),
            "pm10": comps.get("pm10"),
            "nh3": comps.get("nh3"),
            "date": datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
        })

    df = pd.DataFrame(rows)
    print(f"[DEBUG] Transformed {len(df)} rows")
    return df
