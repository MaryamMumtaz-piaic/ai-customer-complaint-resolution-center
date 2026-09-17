from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ComplaintBase(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    subject: str
    description: str
    product_or_service: Optional[str] = None
    order_number: Optional[str] = None
    communication_channel: Optional[str] = "web"

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    assigned_agent_id: Optional[int] = None
    department_id: Optional[int] = None

class Complaint(ComplaintBase):
    id: int
    reference_number: str
    category: Optional[str]
    subcategory: Optional[str]
    priority: str
    status: str
    sentiment: Optional[str]
    urgency: Optional[str]
    assigned_agent_id: Optional[int]
    department_id: Optional[int]
    sla_deadline: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]
    is_escalated: bool
    escalation_count: int

    class Config:
        from_attributes = True
