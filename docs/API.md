# API Reference

This document outlines the primary REST API endpoints available in the backend. 
For interactive testing, run the server and visit `/docs`.

## Base URL
`http://localhost:8000/api`

## Authentication
*(Currently disabled for MVP local dev. Future implementation will require `Authorization: Bearer <token>`)*

---

## Complaints

### `GET /complaints`
Retrieves a list of all complaints.
- **Response**:
```json
{
  "total": 1,
  "items": [
    {
      "id": 1,
      "subject": "Late delivery",
      "status": "open",
      "severity": "high"
    }
  ]
}
```

### `POST /complaints`
Create a new complaint.
- **Request Body**:
```json
{
  "customer_name": "John Doe",
  "email": "john@example.com",
  "subject": "Broken item received",
  "description": "I opened the box and the screen was cracked."
}
```
- **Response**: `201 Created` with created object.

---

## AI Operations

### `POST /ai/draft-response/{complaint_id}`
Generates an AI response for a specific complaint using RAG.
- **Response**:
```json
{
  "draft": "Dear John, I am so sorry to hear that your screen was cracked upon arrival. According to our return policy (Document: return_policy.pdf), we will issue a replacement immediately...",
  "sources": ["return_policy.pdf"]
}
```

### `POST /ai/classify/{complaint_id}`
Triggers AI to analyze sentiment, categorize, and determine severity.
- **Response**:
```json
{
  "category": "Hardware Damage",
  "sentiment": "Angry",
  "severity": "High"
}
```

---

## Knowledge Base

### `POST /knowledge/upload`
Upload a document for the RAG pipeline.
- **Content-Type**: `multipart/form-data`
- **Form Field**: `file` (PDF, TXT)
- **Response**: `{"message": "File uploaded and indexed successfully"}`

## Rate Limiting
Rate limiting is not enforced in the development environment. In production, `/ai/*` endpoints should be limited to prevent excessive OpenAI API billing.
