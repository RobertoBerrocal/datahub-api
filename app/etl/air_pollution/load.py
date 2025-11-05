from app.db import models
from sqlalchemy.orm import Session

def load_air_pollution(df, db: Session):
    for _, row in df.iterrows():
        exists = (
            db.query(models.AirPollutionData)
            .filter_by(city_id=row.city_id, timestamp=row.timestamp)
            .first()
        )
        if not exists:
            db.add(models.AirPollutionData(**row.to_dict()))
    db.commit()
