from app.etl.exchange_rates.transform import transform_exchange_rates


def test_transform_exchange_rates_flattens_rates():
    raw = {
        "base": "USD",
        "rates": {
            "2026-01-01": {"EUR": 0.92, "GBP": 0.79},
            "2026-01-02": {"EUR": 0.93},
        },
    }

    df = transform_exchange_rates(raw)

    assert len(df) == 3
    assert set(df.columns) == {"base_currency", "target_currency", "rate", "date"}
    assert set(df["target_currency"].tolist()) == {"EUR", "GBP"}
