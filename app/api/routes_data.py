from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.db import database, models
from app.etl.exchange_rates.extract import extract_exchange_rates
from app.etl.exchange_rates.transform import transform_exchange_rates
from app.etl.exchange_rates.load import load_exchange_rates
from app.etl.air_pollution.extract import extract_air_pollution
from app.etl.air_pollution.transform import transform_air_pollution
from app.etl.air_pollution.load import load_air_pollution
import time

router = APIRouter()

@router.post("/data/update/exchange_rates")
def update_exchange_rates(db: Session = Depends(database.get_db)):
    bases = ["USD", "EUR"]
    targets = ["GBP", "AUD", "CAD", "PEN", "BRL", "JPY", "CHF", "SEK", "MXN"]
    start_date = "2025-01-01"
    end_date = date.today().strftime("%Y-%m-%d")

    total_rows = 0
    for base in bases:
        raw = extract_exchange_rates(base, targets, start_date, end_date)
        df = transform_exchange_rates(raw)
        load_exchange_rates(df, db)
        total_rows += len(df)

    return {"status": "success", "rows_inserted": total_rows}


@router.post("/data/update/air_pollution")
def update_air_pollution(db: Session = Depends(database.get_db)):
    cities = db.query(models.City).all()
    end = int(time.time())
    start = end - (5 * 24 * 3600)  # Últimos 5 días

    total_rows = 0
    for city in cities:
        raw = extract_air_pollution(city.lat, city.lon, start, end)
        df = transform_air_pollution(raw, city.id)
        load_air_pollution(df, db)
        total_rows += len(df)

    return {"status": "success", "rows_inserted": total_rows}
