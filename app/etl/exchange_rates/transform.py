import pandas as pd

def transform_exchange_rates(data: dict):
    base = data["base_code"]
    date = data["time_last_update_utc"]
    rates = data["rates"]
    rows = [{"base_currency": base, "target_currency": k, "rate": v, "date": date}
            for k, v in rates.items()]
    return pd.DataFrame(rows)
