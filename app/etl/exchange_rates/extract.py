import requests

def extract_exchange_rates(base_currency="EUR"):
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    data = response.json()

    if data.get("result") != "success":
        raise Exception(f"API error: {data.get('error-type', 'Unknown error')}")

    return data

