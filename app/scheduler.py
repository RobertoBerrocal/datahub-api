import logging
from typing import Optional
from datetime import date
from time import perf_counter

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.db.database import SessionLocal

from app.etl.exchange_rates.extract import extract_exchange_rates
from app.etl.exchange_rates.transform import transform_exchange_rates
from app.etl.exchange_rates.load import load_exchange_rates

from app.etl.air_pollution.extract import extract_air_pollution
from app.etl.air_pollution.transform import transform_air_pollution
from app.etl.air_pollution.load import load_air_pollution


logger = logging.getLogger("datahub.scheduler")
logger.setLevel(logging.INFO)

_scheduler: Optional[BackgroundScheduler] = None


def _run_exchange_rates_job() -> None:
    start = perf_counter()
    logger.info("Running scheduled job: exchange_rates")
    bases = ["USD", "EUR"]
    targets = ["GBP", "AUD", "CAD", "PEN", "BRL", "JPY", "CHF", "SEK", "MXN"]
    start_date = "2025-01-01"
    end_date = date.today().strftime("%Y-%m-%d")

    session = SessionLocal()
    try:
        total_rows = 0
        for base in bases:
            raw = extract_exchange_rates(base, targets, start_date, end_date)
            df = transform_exchange_rates(raw)
            total_rows += load_exchange_rates(df, session)
        logger.info(
            "exchange_rates job completed. rows_loaded=%s duration_seconds=%.2f",
            total_rows,
            perf_counter() - start,
        )
    except Exception:
        logger.exception("exchange_rates job failed")
        raise
    finally:
        session.close()


def _run_air_pollution_job() -> None:
    start = perf_counter()
    logger.info("Running scheduled job: air_pollution")
    session = SessionLocal()
    try:
        raw = extract_air_pollution()
        df = transform_air_pollution(raw)
        rows = load_air_pollution(df, session)
        logger.info(
            "air_pollution job completed. rows_loaded=%s duration_seconds=%.2f",
            rows,
            perf_counter() - start,
        )
    except Exception:
        logger.exception("air_pollution job failed")
        raise
    finally:
        session.close()


def init_scheduler() -> None:
    global _scheduler

    if not settings.scheduler_enabled:
        logger.info("Scheduler disabled. Skipping init.")
        return

    if _scheduler is not None:
        logger.info("Scheduler already initialized. Skipping.")
        return

    _scheduler = BackgroundScheduler(timezone=settings.timezone)

    _scheduler.add_job(
        _run_exchange_rates_job,
        trigger=IntervalTrigger(minutes=settings.exchange_rates_interval_minutes),
        id="exchange_rates_job",
        replace_existing=True,
    )

    _scheduler.add_job(
        _run_air_pollution_job,
        trigger=IntervalTrigger(minutes=settings.air_pollution_interval_minutes),
        id="air_pollution_job",
        replace_existing=True,
    )

    _scheduler.start()
    logger.info(
        "Scheduler started. exchange_rates=%sm air_pollution=%sm",
        settings.exchange_rates_interval_minutes,
        settings.air_pollution_interval_minutes,
    )


def is_scheduler_running() -> bool:
    return _scheduler.running if _scheduler is not None else False
