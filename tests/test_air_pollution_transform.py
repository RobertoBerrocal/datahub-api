from app.etl.air_pollution.transform import transform_air_pollution


def test_transform_air_pollution_normalizes_schema():
    raw = [
        {
            "city": "Berlin",
            "lat": 52.52,
            "lon": 13.41,
            "country": "DE",
            "dt": 1710000000,
            "main": {"aqi": 2},
            "components": {
                "co": 1.1,
                "no": 2.2,
                "no2": 3.3,
                "o3": 4.4,
                "so2": 5.5,
                "pm2_5": 6.6,
                "pm10": 7.7,
                "nh3": 8.8,
            },
        }
    ]

    df = transform_air_pollution(raw)

    assert len(df) == 1
    assert "timestamp" in df.columns
    assert "lat" in df.columns
    assert "lon" in df.columns
    assert "country" in df.columns
    assert df.iloc[0]["city"] == "Berlin"
    assert df.iloc[0]["aqi"] == 2
