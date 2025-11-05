from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.db import database
from app.etl.exchange_rates.extract import extract_exchange_rates
from app.etl.exchange_rates.transform import transform_exchange_rates
from app.etl.exchange_rates.load import load_exchange_rates
from app.etl.air_pollution.extract import extract_air_pollution
from app.etl.air_pollution.transform import transform_air_pollution
from app.etl.air_pollution.load import load_air_pollution

router = APIRouter()

# Endpoint to update exchange rates data
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

# Endpoint to update air pollution data
@router.post("/data/update/air_pollution")
def update_air_pollution(db: Session = Depends(database.get_db)):
    try:
        raw = extract_air_pollution()
        df = transform_air_pollution(raw)
        rows = load_air_pollution(df, db)
        return {"status": "success", "rows_inserted": rows}
    except Exception as e:
        return {"status": "error", "message": str(e)}