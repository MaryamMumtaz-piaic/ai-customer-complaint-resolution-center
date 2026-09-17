from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..database import get_db
from ..services.ai_service import classify_complaint, generate_response, generate_business_insights
from ..services.rag_service import get_relevant_context
from ..models.complaint import Complaint

router = APIRouter(prefix="/ai", tags=["ai"])

class ClassifyRequest(BaseModel):
    subject: str
    description: str
    category_hint: Optional[str] = None

@router.post("/classify")
def classify(req: ClassifyRequest):
    return classify_complaint(req.subject, req.description, req.category_hint)

class GenerateResponseRequest(BaseModel):
    complaint_id: int
    tone: str = "professional"
    channel: str = "email"

@router.post("/generate-response")
def generate_draft(req: GenerateResponseRequest, db: Session = Depends(get_db)):
    comp = db.query(Complaint).filter(Complaint.id == req.complaint_id).first()
    if not comp:
        raise HTTPException(404, "Complaint not found")
        
    complaint_data = {
        "subject": comp.subject,
        "description": comp.description,
        "category": comp.category
    }
    
    context = get_relevant_context(db, comp.description)
    response_text = generate_response(complaint_data, context, req.tone, req.channel)
    
    return {"draft": response_text, "context_used": context != ""}

class InsightsRequest(BaseModel):
    analytics_data: Dict[str, Any]

@router.post("/insights")
def insights(req: InsightsRequest):
    return {"insights": generate_business_insights(req.analytics_data)}

@router.post("/root-cause")
def root_cause(req: InsightsRequest):
    # Dummy implementation for MVP
    return {"analysis": "Root cause analysis based on provided data..."}
