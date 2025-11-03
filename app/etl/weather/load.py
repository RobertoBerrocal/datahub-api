from app.db.database import engine
import pandas as pd

def load_weather_data(df: pd.DataFrame):
    df.to_sql("weather", con=engine, if_exists="append", index=False)
