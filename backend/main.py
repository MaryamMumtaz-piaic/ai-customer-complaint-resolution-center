from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from config import settings
from database import engine, Base, get_db
from routers import (
    users, complaints, documents, ai, analytics, escalations, resolutions
)
from models.user import User, Department
from models.complaint import Complaint
from models.document import Document
from models.resolution import Resolution

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Customer Complaint Resolution Center API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files if needed, just a placeholder path for now
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(users.router, prefix="/api")
app.include_router(users.dept_router, prefix="/api")
app.include_router(complaints.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(escalations.router, prefix="/api")
app.include_router(resolutions.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    # Seed data if empty
    if db.query(Department).count() == 0:
        d1 = Department(name="Technical Support", description="Tech issues")
        d2 = Department(name="Billing & Finance", description="Money matters")
        d3 = Department(name="Customer Relations", description="General inquiries")
        db.add_all([d1, d2, d3])
        db.commit()

        u1 = User(name="Admin User", email="admin@company.com", role="admin", department_id=d1.id)
        u2 = User(name="Agent Smith", email="agent@company.com", role="support_agent", department_id=d1.id)
        u3 = User(name="Manager Jane", email="manager@company.com", role="manager", department_id=d1.id)
        db.add_all([u1, u2, u3])
        db.commit()
        
        # Seed complaints
        for i in range(5):
            c = Complaint(
                customer_name=f"Customer {i}",
                customer_email=f"cust{i}@test.com",
                subject=f"Issue {i}",
                description=f"Description of issue {i}",
                status=["new", "in_progress", "resolved", "escalated", "new"][i]
            )
            db.add(c)
        db.commit()

@app.get("/health")
def health_check():
    return {"status": "ok"}
