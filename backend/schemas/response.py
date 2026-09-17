from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResponseDraftBase(BaseModel):
    content: str
    tone: Optional[str] = None
    channel: Optional[str] = None

class ResponseDraftCreate(ResponseDraftBase):
    complaint_id: int
    generated_by_ai: bool = True

class ResponseDraft(ResponseDraftBase):
    id: int
    complaint_id: int
    status: str
    generated_by_ai: bool
    reviewed_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ResolutionBase(BaseModel):
    complaint_id: int
    category: Optional[str] = None
    original_complaint_summary: Optional[str] = None
    final_response: Optional[str] = None
    resolution_type: Optional[str] = None
    department_id: Optional[int] = None
    time_to_resolution_hours: Optional[int] = None
    customer_outcome: Optional[str] = None
    internal_notes: Optional[str] = None

class ResolutionCreate(ResolutionBase):
    pass

class Resolution(ResolutionBase):
    id: int
    created_by_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
