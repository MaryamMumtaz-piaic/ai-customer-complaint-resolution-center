from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.complaint import Complaint, ComplaintEvent, CommunicationRecord
from ..schemas.complaint import Complaint as ComplaintSchema, ComplaintCreate, ComplaintUpdate
from pydantic import BaseModel
from ..services.escalation_service import check_and_escalate

router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.get("", response_model=List[ComplaintSchema])
def list_complaints(status: Optional[str] = None, priority: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Complaint)
    if status:
        query = query.filter(Complaint.status == status)
    if priority:
        query = query.filter(Complaint.priority == priority)
    return query.all()

@router.post("", response_model=ComplaintSchema)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    db_complaint = Complaint(**complaint.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    # Check if needs auto-escalation
    check_and_escalate(db, db_complaint.id)
    return db_complaint

@router.get("/{id}", response_model=ComplaintSchema)
def get_complaint(id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.put("/{id}", response_model=ComplaintSchema)
def update_complaint(id: int, update_data: ComplaintUpdate, db: Session = Depends(get_db)):
    db_complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_complaint, key, value)
    
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

class StatusUpdate(BaseModel):
    status: str
    reason: Optional[str] = None
    user_id: Optional[int] = None

@router.post("/{id}/status")
def change_status(id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    comp = db.query(Complaint).filter(Complaint.id == id).first()
    if not comp:
        raise HTTPException(404, "Not found")
        
    old_status = comp.status
    comp.status = status_update.status
    
    event = ComplaintEvent(
        complaint_id=id,
        event_type="status_change",
        previous_status=old_status,
        new_status=status_update.status,
        reason=status_update.reason,
        changed_by_id=status_update.user_id
    )
    db.add(event)
    db.commit()
    return {"message": "Status updated"}

class EscalateRequest(BaseModel):
    reason: str
    user_id: Optional[int] = None

@router.post("/{id}/escalate")
def escalate_complaint(id: int, req: EscalateRequest, db: Session = Depends(get_db)):
    comp = db.query(Complaint).filter(Complaint.id == id).first()
    if not comp:
        raise HTTPException(404, "Not found")
    
    comp.is_escalated = True
    comp.escalation_count += 1
    comp.status = "escalated"
    db.commit()
    return {"message": "Escalated"}

@router.get("/{id}/events")
def get_events(id: int, db: Session = Depends(get_db)):
    return db.query(ComplaintEvent).filter(ComplaintEvent.complaint_id == id).all()

@router.get("/{id}/communications")
def get_communications(id: int, db: Session = Depends(get_db)):
    return db.query(CommunicationRecord).filter(CommunicationRecord.complaint_id == id).all()
