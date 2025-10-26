from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, database

router = APIRouter()

@router.get("/data/sources")
def list_sources(db: Session = Depends(database.get_db)):
    sources = db.query(models.DataSource).all()
    return [{"id": s.id, "name": s.name, "description": s.description} for s in sources]
