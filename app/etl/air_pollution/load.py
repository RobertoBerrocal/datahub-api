import logging
from sqlalchemy.orm import Session

from app.db import models, database

logger = logging.getLogger("datahub.air_pollution.load")


def load_air_pollution(df, db: Session | None = None):
    if df.empty:
        return 0

    owns_session = db is None
    session = db or database.SessionLocal()

    try:
        city_name_to_id: dict[str, int] = {}
        inserted = 0

        for city_name in df["city"].unique():
            city = session.query(models.City).filter_by(name=city_name).first()
            if city is None:
                city = models.City(name=city_name, lat=0.0, lon=0.0, country="N/A")
                session.add(city)
                session.flush()
            city_name_to_id[city_name] = city.id

        for _, row in df.iterrows():
            city_id = city_name_to_id[row.city]
            exists = (
                session.query(models.AirPollutionData)
                .filter_by(city_id=city_id, timestamp=row.timestamp)
                .first()
            )
            if exists:
                continue

            session.add(
                models.AirPollutionData(
                    city_id=city_id,
                    aqi=row.aqi,
                    co=row.co,
                    no=row.no,
                    no2=row.no2,
                    o3=row.o3,
                    so2=row.so2,
                    pm2_5=row.pm2_5,
                    pm10=row.pm10,
                    nh3=row.nh3,
                    timestamp=row.timestamp,
                )
            )
            inserted += 1

        session.commit()
        logger.info("Inserted %s rows into air_pollution_data", inserted)
        return inserted
    finally:
        if owns_session:
            session.close()
