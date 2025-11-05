from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint
from app.db.database import Base

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String, index=True)
    target_currency = Column(String, index=True)
    rate = Column(Float)
    date = Column(Date, index=True)
    __table_args__ = (UniqueConstraint("base_currency", "target_currency", "date", name="_exchange_unique"),)


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    lat = Column(Float)
    lon = Column(Float)
    country = Column(String)


class AirPollutionData(Base):
    __tablename__ = "air_pollution_data"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    aqi = Column(Integer)
    co = Column(Float)
    no = Column(Float)
    no2 = Column(Float)
    o3 = Column(Float)
    so2 = Column(Float)
    pm2_5 = Column(Float)
    pm10 = Column(Float)
    nh3 = Column(Float)
    timestamp = Column(DateTime, index=True)
    __table_args__ = (UniqueConstraint("city_id", "timestamp", name="_city_timestamp_unique"),)
