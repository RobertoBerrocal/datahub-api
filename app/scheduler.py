import logging
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings

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
    logger.info("Running scheduled job: exchange_rates")
    raw = extract_exchange_rates()
    df = transform_exchange_rates(raw)
    rows = load_exchange_rates(df)
    logger.info("exchange_rates job completed. rows_loaded=%s", rows)


def _run_air_pollution_job() -> None:
    logger.info("Running scheduled job: air_pollution")
    raw = extract_air_pollution()
    df = transform_air_pollution(raw)
    rows = load_air_pollution(df)
    logger.info("air_pollution job completed. rows_loaded=%s", rows)


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
