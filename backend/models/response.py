from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from ..database import Base

class ResponseDraft(Base):
    __tablename__ = "response_drafts"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    content = Column(Text, nullable=False)
    tone = Column(String)
    channel = Column(String)
    status = Column(String, default="draft") # draft, approved, rejected, sent
    
    generated_by_ai = Column(Boolean, default=True)
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CommunicationRecord(Base):
    __tablename__ = "communication_records"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    channel = Column(String, nullable=False)
    direction = Column(String, nullable=False) # inbound, outbound
    
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    recipient_info = Column(String)
    status = Column(String)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
