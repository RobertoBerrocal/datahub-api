from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
import pandas as pd

Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String)
    target_currency = Column(String)
    rate = Column(Float)
    date = Column(String)

def load_exchange_rates(df: pd.DataFrame):
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    df.to_sql("exchange_rates", con=engine, if_exists="replace", index=False)
