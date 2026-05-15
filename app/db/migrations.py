import logging

from sqlalchemy import inspect, text

from app.db.database import engine

logger = logging.getLogger("datahub.db.migrations")


def _create_air_pollution_table(conn) -> None:
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS air_pollution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_id INTEGER,
                aqi INTEGER,
                co FLOAT,
                no FLOAT,
                no2 FLOAT,
                o3 FLOAT,
                so2 FLOAT,
                pm2_5 FLOAT,
                pm10 FLOAT,
                nh3 FLOAT,
                timestamp DATETIME,
                UNIQUE(city_id, timestamp),
                FOREIGN KEY(city_id) REFERENCES cities(id)
            )
            """
        )
    )


def _migrate_legacy_city_date_table(conn, source_table: str) -> None:
    _create_air_pollution_table(conn)
    conn.execute(
        text(
            f"""
            INSERT OR IGNORE INTO cities (name, lat, lon, country)
            SELECT DISTINCT city, 0.0, 0.0, 'N/A'
            FROM {source_table}
            WHERE city IS NOT NULL
            """
        )
    )
    conn.execute(
        text(
            f"""
            INSERT OR IGNORE INTO air_pollution (
                city_id, aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3, timestamp
            )
            SELECT
                c.id,
                ap.aqi,
                ap.co,
                ap.no,
                ap.no2,
                ap.o3,
                ap.so2,
                ap.pm2_5,
                ap.pm10,
                ap.nh3,
                ap.date
            FROM {source_table} ap
            LEFT JOIN cities c ON c.name = ap.city
            """
        )
    )


def _migrate_normalized_table(conn, source_table: str) -> None:
    _create_air_pollution_table(conn)
    conn.execute(
        text(
            f"""
            INSERT OR IGNORE INTO air_pollution (
                city_id, aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3, timestamp
            )
            SELECT city_id, aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3, timestamp
            FROM {source_table}
            """
        )
    )


def run_startup_migrations() -> None:
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "air_pollution_data" not in tables:
        return

    columns = {column["name"] for column in inspector.get_columns("air_pollution_data")}
    logger.warning("Found legacy table air_pollution_data. Running rename/migration to air_pollution.")

    with engine.begin() as conn:
        if {"id", "city_id", "timestamp"}.issubset(columns) and "air_pollution" not in tables:
            conn.execute(text("ALTER TABLE air_pollution_data RENAME TO air_pollution"))
            logger.info("Renamed air_pollution_data to air_pollution.")
            return

        if {"city", "date"}.issubset(columns):
            _migrate_legacy_city_date_table(conn, "air_pollution_data")
        else:
            _migrate_normalized_table(conn, "air_pollution_data")

        conn.execute(text("DROP TABLE air_pollution_data"))
        logger.info("Migrated and removed legacy table air_pollution_data.")
