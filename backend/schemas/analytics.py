from pydantic import BaseModel
from typing import Dict, Any, List

class DashboardStats(BaseModel):
    total_complaints: int
    active_complaints: int
    resolved_complaints: int
    escalated_complaints: int
    avg_resolution_time_hours: float

class TrendData(BaseModel):
    date: str
    count: int

class CategoryBreakdown(BaseModel):
    category: str
    count: int
