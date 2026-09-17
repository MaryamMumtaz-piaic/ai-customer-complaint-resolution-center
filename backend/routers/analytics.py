from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.analytics_service import get_dashboard_stats
from ..schemas.analytics import DashboardStats

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard", response_model=DashboardStats)
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)

@router.get("/trends")
def trends(db: Session = Depends(get_db)):
    return [{"date": "2023-01-01", "count": 10}, {"date": "2023-01-02", "count": 15}]

@router.get("/categories")
def categories(db: Session = Depends(get_db)):
    return [{"category": "Technical", "count": 25}, {"category": "Billing", "count": 15}]

@router.get("/departments")
def departments(db: Session = Depends(get_db)):
    return [{"department": "Tech Support", "workload": 40}]

@router.get("/recurring")
def recurring(db: Session = Depends(get_db)):
    return [{"pattern": "Login Issues", "frequency": 12}]

@router.get("/resolution-times")
def resolution_times(db: Session = Depends(get_db)):
    return [{"category": "Technical", "avg_time": 48.5}]
