from app.db.database import engine  # Importamos el engine directamente

def load_air_pollution(df, _db=None):
    if df.empty:
        print("[WARN] Empty dataframe, skipping load.")
        return 0

    df.to_sql("air_pollution_data", con=engine, if_exists="append", index=False)
    print(f"[INFO] Inserted {len(df)} rows into air_pollution_data.")
    return len(df)
