from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.complaint import Complaint
from typing import Dict, Any

def get_dashboard_stats(db: Session) -> Dict[str, Any]:
    total = db.query(Complaint).count()
    active = db.query(Complaint).filter(Complaint.status.notin_(["resolved", "closed"])).count()
    resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"])).count()
    escalated = db.query(Complaint).filter(Complaint.is_escalated == True).count()
    
    # Calculate dummy avg resolution time for MVP
    avg_res_time = 24.5
    
    return {
        "total_complaints": total,
        "active_complaints": active,
        "resolved_complaints": resolved,
        "escalated_complaints": escalated,
        "avg_resolution_time_hours": avg_res_time
    }
