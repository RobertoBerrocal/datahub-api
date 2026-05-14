import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes_data import router as data_router
from app.db import models, database
from app.scheduler import init_scheduler, is_scheduler_running, shutdown_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    init_scheduler()
    try:
        yield
    finally:
        shutdown_scheduler()


app = FastAPI(title="DataHub API", lifespan=lifespan)

app.include_router(data_router)

@app.get("/")
def root():
    return {"message": "Welcome to DataHub API 🚀"}


@app.get("/health")
def health():
    db_ok = True
    try:
        with database.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    return {
        "status": "ok" if db_ok else "degraded",
        "database": "ok" if db_ok else "error",
        "scheduler_running": is_scheduler_running(),
    }
