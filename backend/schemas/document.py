from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    file_type: str
    original_filename: str
    file_path: str
    status: str
    chunk_count: int
    source_metadata: Optional[Dict[str, Any]] = None
    uploaded_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
