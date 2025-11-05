import pandas as pd

def transform_exchange_rates(raw_data: dict):
    base = raw_data["base"]
    records = []
    for date_str, rates in raw_data["rates"].items():
        for target, rate in rates.items():
            records.append({
                "base_currency": base,
                "target_currency": target,
                "rate": rate,
                "date": pd.to_datetime(date_str).date()
            })
    return pd.DataFrame(records)
