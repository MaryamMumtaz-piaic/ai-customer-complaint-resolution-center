from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.resolution import Resolution
from ..schemas.response import Resolution as ResolutionSchema, ResolutionCreate
from typing import List

router = APIRouter(prefix="/resolutions", tags=["resolutions"])

@router.get("", response_model=List[ResolutionSchema])
def list_resolutions(db: Session = Depends(get_db)):
    return db.query(Resolution).all()

@router.post("", response_model=ResolutionSchema)
def create_resolution(res: ResolutionCreate, db: Session = Depends(get_db)):
    db_res = Resolution(**res.model_dump())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

@router.get("/{id}", response_model=ResolutionSchema)
def get_resolution(id: int, db: Session = Depends(get_db)):
    res = db.query(Resolution).filter(Resolution.id == id).first()
    if not res:
        raise HTTPException(404, "Not found")
    return res
