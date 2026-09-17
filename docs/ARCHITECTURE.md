# Architecture Overview

ComplaintIQ is structured as a decoupled web application with a stateless backend API and a static frontend.

## System Architecture

```text
[ Browser / User ]
       |
       | (HTTP/JSON over REST)
       v
[ FastAPI Application (Backend) ]
       |
       +---> [ SQLite Database ] (Relational Data: Complaints, Users)
       |
       +---> [ Vector Store ] (FAISS/Chroma: Embeddings for RAG)
       |
       +---> [ OpenAI API ] (LLM & Embeddings Generation)
```

## Data Flow Diagram

**1. Complaint Intake:**
Customer Submits -> Backend API -> Saved to DB -> AI Analyzes Sentiment & Priority -> DB Updated.

**2. RAG Document Ingestion:**
Admin Uploads PDF -> Backend Extracts Text -> Text Chunked -> Chunks Embedded via OpenAI -> Stored in Vector DB.

**3. AI Response Generation:**
Agent Requests Draft -> Backend Queries Vector DB with Complaint Context -> Relevant Chunks Retrieved -> Prompt Constructed with Chunks + Complaint -> OpenAI GPT-4o-mini Drafts Response -> Draft Returned to UI.

## RAG (Retrieval-Augmented Generation) Pipeline
- **Embedding Model**: `text-embedding-3-small`.
- **Chunking Strategy**: 500 tokens per chunk with 50 token overlap to maintain context continuity.
- **Retrieval Metric**: Cosine similarity. Top 3-5 most relevant chunks are injected into the LLM system prompt.

## Database Schema (Relational)
- **Complaints**: `id`, `customer_name`, `email`, `subject`, `description`, `status`, `severity`, `created_at`.
- **KnowledgeBase**: `id`, `filename`, `upload_date`, `status` (indexed/pending).
- **Users**: `id`, `username`, `role` (admin/agent), `password_hash`.

## API Structure
The API is fully RESTful.
- `/api/complaints`: CRUD operations for complaints.
- `/api/knowledge`: Document management and indexing triggers.
- `/api/ai`: Endpoints for classification and generation.
- `/api/analytics`: Aggregation endpoints for dashboard charts.
