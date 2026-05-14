import logging

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes_data import router as data_router
from app.db import models, database
from app.scheduler import init_scheduler, is_scheduler_running

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(title="DataHub API")

app.include_router(data_router)

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)
    init_scheduler()

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
