from app.db import models, database
from sqlalchemy.orm import Session
from sqlalchemy import tuple_

def load_exchange_rates(df, db: Session | None = None):
    if df.empty:
        return 0

    owns_session = db is None
    session = db or database.SessionLocal()

    try:
        unique_keys = {
            (row.base_currency, row.target_currency, row.date)
            for _, row in df.iterrows()
        }

        existing = set(
            session.query(
                models.ExchangeRate.base_currency,
                models.ExchangeRate.target_currency,
                models.ExchangeRate.date,
            )
            .filter(
                tuple_(
                    models.ExchangeRate.base_currency,
                    models.ExchangeRate.target_currency,
                    models.ExchangeRate.date,
                ).in_(unique_keys)
            )
            .all()
        )

        rows_to_insert = []
        for _, row in df.iterrows():
            key = (row.base_currency, row.target_currency, row.date)
            if key not in existing:
                rows_to_insert.append(models.ExchangeRate(**row.to_dict()))

        if rows_to_insert:
            session.add_all(rows_to_insert)
            session.commit()

        return len(rows_to_insert)
    finally:
        if owns_session:
            session.close()
