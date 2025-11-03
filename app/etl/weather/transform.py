import pandas as pd

def transform_weather_data(data: dict):
    main = data["main"]
    wind = data.get("wind", {})
    weather = data["weather"][0]

    df = pd.DataFrame([{
        "city": data["name"],
        "temperature": main["temp"],
        "humidity": main["humidity"],
        "pressure": main["pressure"],
        "wind_speed": wind.get("speed", None),
        "description": weather["description"],
        "timestamp": data["dt"]
    }])
    return df
