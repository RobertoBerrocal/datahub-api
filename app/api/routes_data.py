from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, database
from app.etl.exchange_rates.extract import extract_exchange_rates
from app.etl.exchange_rates.transform import transform_exchange_rates
from app.etl.exchange_rates.load import load_exchange_rates

router = APIRouter()

@router.get("/data/sources")
def list_sources(db: Session = Depends(database.get_db)):
    sources = db.query(models.DataSource).all()
    return [{"id": s.id, "name": s.name, "description": s.description} for s in sources]
@router.post("/data/update/exchange_rates")
def update_exchange_rates():
    try:
        raw = extract_exchange_rates()
        df = transform_exchange_rates(raw)
        load_exchange_rates(df)
        return {"status": "success", "rows": len(df), "message": "Exchange rates updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
