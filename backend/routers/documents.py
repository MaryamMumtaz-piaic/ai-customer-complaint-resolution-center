from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.document import Document
from ..schemas.document import Document as DocumentSchema
from ..services.rag_service import process_document
import os
import shutil

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("", response_model=List[DocumentSchema])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.post("/upload", response_model=DocumentSchema)
async def upload_document(
    name: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    ext = file.filename.split('.')[-1] if '.' in file.filename else ''
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    doc = Document(
        name=name,
        description=description,
        file_type=ext,
        original_filename=file.filename,
        file_path=file_path
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Process asynchronously in real app, sync here for MVP
    process_document(db, doc.id)
    
    return doc

@router.get("/{id}", response_model=DocumentSchema)
def get_document(id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == id).first()
    if not doc:
        raise HTTPException(404, "Not found")
    return doc

@router.delete("/{id}")
def delete_document(id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == id).first()
    if not doc:
        raise HTTPException(404, "Not found")
    db.delete(doc)
    db.commit()
    return {"message": "Deleted"}

@router.post("/{id}/reprocess")
def reprocess_document(id: int, db: Session = Depends(get_db)):
    success = process_document(db, id)
    return {"success": success}
