import requests
from datetime import datetime
from app.core.config import settings

BASE_URL = "https://api.frankfurter.app"

def extract_exchange_rates(base_currency: str, targets: list[str], start_date: str, end_date: str):
    url = f"{BASE_URL}/{start_date}..{end_date}?base={base_currency}&to={','.join(targets)}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data
