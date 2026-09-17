from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4())[:8].upper())
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String)
    
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    product_or_service = Column(String)
    order_number = Column(String)
    
    category = Column(String)
    subcategory = Column(String)
    priority = Column(String, default="medium") # low, medium, high, critical
    status = Column(String, default="new") # new, under_review, assigned, waiting_for_customer, escalated, in_progress, resolved, closed, reopened
    
    sentiment = Column(String)
    urgency = Column(String)
    communication_channel = Column(String, default="web")
    
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    sla_deadline = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    is_escalated = Column(Boolean, default=False)
    escalation_count = Column(Integer, default=0)

    assigned_agent = relationship("User", foreign_keys=[assigned_agent_id])
    department = relationship("Department", foreign_keys=[department_id])
    events = relationship("ComplaintEvent", back_populates="complaint")

class ComplaintEvent(Base):
    __tablename__ = "complaint_events"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    event_type = Column(String, nullable=False)
    previous_status = Column(String)
    new_status = Column(String)
    changed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reason = Column(String)
    internal_note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    complaint = relationship("Complaint", back_populates="events")

class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    reason = Column(Text, nullable=False)
    escalated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    escalation_deadline = Column(DateTime(timezone=True))
    status = Column(String, default="pending")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
