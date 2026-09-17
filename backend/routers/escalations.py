from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.complaint import Escalation

router = APIRouter(prefix="/escalations", tags=["escalations"])

@router.get("")
def list_escalations(db: Session = Depends(get_db)):
    return db.query(Escalation).all()
