import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "datahub.db"

if not DB_PATH.exists():
    DB_PATH = BASE_DIR.parent / "data" / "datahub.db"

if not DB_PATH.exists():
    raise FileNotFoundError(f"[ERROR] No se encontró la base de datos en {DB_PATH}")


def run_query(query: str) -> pd.DataFrame:
    print(f"[DEBUG] Using DB at: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn)
        print(f"[DEBUG] Query executed successfully. Rows returned: {len(df)}")
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        raise
    finally:
        conn.close()

    return df
