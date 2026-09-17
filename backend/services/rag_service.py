import openai
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from ..models.document import Document, DocumentChunk
from ..config import settings
from .document_processor import process_file
import numpy as np

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    # Very simple word-based chunker for MVP
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def get_embedding(text: str) -> List[float]:
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(
            input=text,
            model=settings.EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        # Return random embedding for local testing if API key fails
        return list(np.random.rand(1536))

def process_document(db: Session, document_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        return False
    
    text = process_file(doc.file_path, doc.file_type)
    if not text:
        doc.status = "failed"
        db.commit()
        return False
        
    chunks = chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
    
    for i, chunk_content in enumerate(chunks):
        embedding = get_embedding(chunk_content)
        db_chunk = DocumentChunk(
            document_id=doc.id,
            chunk_index=i,
            content=chunk_content,
            embedding=embedding
        )
        db.add(db_chunk)
        
    doc.chunk_count = len(chunks)
    doc.status = "ready"
    db.commit()
    return True

def cosine_similarity(a: List[float], b: List[float]) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_relevant_chunks(db: Session, query: str, top_k: int = 5) -> List[DocumentChunk]:
    query_embedding = get_embedding(query)
    
    chunks = db.query(DocumentChunk).all()
    if not chunks:
        return []
        
    scored_chunks = []
    for chunk in chunks:
        if chunk.embedding:
            score = cosine_similarity(query_embedding, chunk.embedding)
            scored_chunks.append((score, chunk))
            
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:top_k]]

def get_relevant_context(db: Session, query: str) -> str:
    chunks = retrieve_relevant_chunks(db, query)
    context = ""
    for idx, chunk in enumerate(chunks):
        doc = chunk.document
        context += f"Source [{idx+1}] - {doc.name}:\n{chunk.content}\n\n"
    return context
