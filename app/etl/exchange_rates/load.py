from app.db import models, database
from sqlalchemy.orm import Session
from sqlalchemy import func

def load_exchange_rates(df, db: Session):
    for _, row in df.iterrows():
        exists = (
            db.query(models.ExchangeRate)
            .filter_by(base_currency=row.base_currency,
                       target_currency=row.target_currency,
                       date=row.date)
            .first()
        )
        if not exists:
            db.add(models.ExchangeRate(**row.to_dict()))
    db.commit()
