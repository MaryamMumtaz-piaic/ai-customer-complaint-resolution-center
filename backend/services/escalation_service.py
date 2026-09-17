from sqlalchemy.orm import Session
from ..models.complaint import Complaint, Escalation
from ..services.ai_service import detect_escalation_triggers

def check_and_escalate(db: Session, complaint_id: int):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint or complaint.is_escalated:
        return
        
    complaint_data = {
        "description": complaint.description,
        "sentiment": complaint.sentiment,
        "priority": complaint.priority,
        "escalation_count": complaint.escalation_count
    }
    
    analysis = detect_escalation_triggers(complaint_data)
    if analysis.get("should_escalate"):
        complaint.is_escalated = True
        complaint.escalation_count += 1
        complaint.status = "escalated"
        
        esc = Escalation(
            complaint_id=complaint.id,
            reason=analysis.get("reason", "AI detected escalation trigger")
        )
        db.add(esc)
        db.commit()
