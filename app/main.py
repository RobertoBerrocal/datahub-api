from fastapi import FastAPI
from app.api.routes_data import router as data_router
from app.db import models, database

app = FastAPI(title="DataHub API")

app.include_router(data_router)

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Welcome to DataHub API 🚀"}
