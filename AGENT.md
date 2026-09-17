# AGENT.md - Agentic Coding Guidelines for ComplaintIQ

## Overview
This document provides rigid guardrails and operational guidelines for autonomous AI coding agents (Antigravity, Cursor, Copilot Workspace, etc.) when manipulating the ComplaintIQ codebase.

## Repository Map
- `/backend`: Contains all Python code, FastAPI routes, DB models, and AI logic.
  - `/api`: FastAPI routers (endpoints).
  - `/models`: SQLAlchemy models representing DB tables.
  - `/schemas`: Pydantic models for request/response validation.
  - `/services`: Core business logic, OpenAI calls, RAG processing.
- `/frontend`: Contains all static assets served to the client.
  - `/css`: Tailwind stylesheets.
  - `/js`: Client-side logic, API connection wrappers.
- `/docs`: Markdown files describing architecture, deployment, and API contracts.

## Task Types

### Adding a New API Endpoint
1. Define the Pydantic request and response schemas in `backend/schemas/`.
2. Implement the core logic in a function inside `backend/services/`.
3. Create the route in the appropriate file in `backend/api/`, injecting the DB session and calling the service function.
4. Update `docs/API.md` with the new endpoint details.

### Adding a New Frontend Page
1. Create the `.html` file in `frontend/`.
2. Link the standard `app.css` and relevant JS files.
3. Ensure the navigation sidebar includes a link to the new page.
4. Implement UI utilizing Tailwind utility classes.
5. Implement logic in a new `frontend/js/<page_name>.js` file.

### Modifying the RAG Pipeline
1. Modifications to chunking or embedding should be localized to `backend/services/ai_service.py`.
2. Ensure you do not change the underlying embedding dimension (1536 for text-embedding-3-small) without planning a full vector database wipe and re-index.
3. Test with local text files to verify retrieval accuracy.

### Adding a New Database Model
1. Define the SQLAlchemy class in `backend/models/`.
2. Ensure relationships (`relationship()`) and foreign keys are explicitly defined.
3. Add the corresponding Pydantic schema for serialization.
4. Restart the backend to allow `Base.metadata.create_all()` to create the table.

## Constraints
- **DO NOT** modify `.env` files programmatically.
- **DO NOT** hardcode API keys anywhere in the codebase. Use `os.getenv()`.
- **ALWAYS** implement fallback logic. If `OPENAI_API_KEY` is None, return a graceful error or mock data.
- **Frontend Constraints**: Use Tailwind classes exclusively for styling. Do not write custom CSS in `app.css` unless it is a global utility or overriding a browser default.
- **Backend Constraints**: All business logic must reside in `services/`. FastApi routers (`api/`) must only handle HTTP routing, dependency injection, and returning responses.

## File Naming Conventions
- Python files: `snake_case.py`
- JavaScript files: `kebab-case.js` or `camelCase.js`
- HTML files: `kebab-case.html`
- Database Models: `PascalCase` (e.g., `ComplaintLog`)
- API endpoints: plural nouns (`/api/complaints`, not `/api/complaint`)

## API Contract
- Standard response format for lists: `{"items": [...], "total": int}`
- Error format: `{"detail": "Clear error message"}` with appropriate HTTP status codes (400, 404, 500).
- Dates must be transmitted in ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`).

## Dependency Management
- **Python**: Append any new pip packages to `backend/requirements.txt` with version pins (e.g., `package==1.2.3`).
- **Frontend**: Do not introduce npm, yarn, webpack, or vite. Use CDNs (like unpkg or cdnjs) via `<script>` tags for external libraries.

## Before Committing / Completing Task
- [ ] No API keys or secrets in the code.
- [ ] `requirements.txt` updated if backend dependencies changed.
- [ ] New endpoints documented in `docs/API.md`.
- [ ] CORS headers verified if new frontend origins were added.
- [ ] Appropriate `try/except` blocks in place for external API calls and DB operations.
