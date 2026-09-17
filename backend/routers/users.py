from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, Department
from ..schemas.user import User as UserSchema, UserCreate, Department as DepartmentSchema, DepartmentCreate

router = APIRouter(prefix="/users", tags=["users"])
dept_router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("", response_model=List[UserSchema])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@dept_router.get("", response_model=List[DepartmentSchema])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@dept_router.post("", response_model=DepartmentSchema)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    db_dept = Department(**dept.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept
