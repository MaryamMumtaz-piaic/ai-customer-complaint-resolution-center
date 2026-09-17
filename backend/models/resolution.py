from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base

class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    category = Column(String)
    original_complaint_summary = Column(Text)
    final_response = Column(Text)
    
    resolution_type = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    time_to_resolution_hours = Column(Integer)
    customer_outcome = Column(String)
    
    internal_notes = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
