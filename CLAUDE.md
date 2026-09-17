# CLAUDE.md - AI Assistant Guidelines for ComplaintIQ

## Project Identity
**Name**: AI Customer Complaint Resolution Center (ComplaintIQ)
**Purpose**: Help companies manage, analyze, resolve, and learn from customer complaints using RAG-powered AI.
**Tech Stack**: HTML5/Vanilla JS/Tailwind (Frontend), Python/FastAPI/SQLAlchemy (Backend), SQLite (DB), OpenAI GPT-4o-mini & Embeddings.

## Architecture Overview
- **Backend**: FastAPI modular structure. `routers/` handle HTTP requests, `services/` contain business and AI logic, `models/` contain SQLAlchemy definitions, `schemas/` contain Pydantic validation.
- **Frontend**: MPA (Multi-Page Application) using semantic HTML and Vanilla JS. Heavy reliance on modern browser features (fetch, ES6). No build step required for JS.
- **RAG Pipeline**: Documents uploaded are parsed, chunked, embedded using OpenAI's `text-embedding-3-small`, and stored in a local vector database. When a complaint arrives, semantic search retrieves relevant chunks to form context for `GPT-4o-mini`.

## Development Commands
### Backend
- Start server: `cd backend && uvicorn main:app --reload --port 8000`
- Install deps: `pip install -r requirements.txt`
- Reset database: delete `complaint_center.db` and restart server.

### Frontend
- Serve frontend: `python -m http.server 5500 --directory frontend`
- Or use VS Code Live Server extension

## Key Files
- `backend/main.py`: FastAPI app initialization and CORS setup.
- `backend/services/ai_service.py`: OpenAI integration and RAG logic.
- `backend/models/database.py`: SQLAlchemy session and declarative base.
- `frontend/js/api.js`: Centralized fetch wrappers and API endpoint definitions.
- `frontend/app.css`: Custom CSS overriding or extending Tailwind.

## Code Style Guidelines
- **Python**: Follow PEP 8 strictly. Use type hints (`def get_item(item_id: int) -> Item:`). Add descriptive docstrings on all functions and classes.
- **JavaScript**: Use ES6+ features. Prefer `async/await` over `.then()`. Use meaningful, camelCase variable names. Wrap DOM manipulation in `DOMContentLoaded` listeners.
- **HTML**: Semantic HTML5 tags (`<main>`, `<section>`, `<article>`). Use utility classes from Tailwind CSS.
- **SQL**: Never write raw SQL. Use SQLAlchemy ORM (`db.query(Model).filter()`).

## AI Integration Notes
- OpenAI API key is strictly stored in `.env` and loaded via `os.getenv()`, never hardcoded.
- **Fallback**: When the API key is missing or invalid, functions must return graceful fallback responses (e.g., "AI features currently disabled") instead of crashing the app.
- **RAG Configuration**: Default chunk size is 500 tokens, overlap is 50 tokens.
- **Citations**: Always append source file names/references to AI-generated responses based on retrieved context.
- **Human-in-the-Loop**: AI responses are drafted, but always require explicit human approval via the UI before being marked as "sent".

## Database
- SQLite is used for development (`complaint_center.db`).
- Code must be written in a database-agnostic way so it can be easily migrated to PostgreSQL for production.
- Run migrations via SQLAlchemy `Base.metadata.create_all(bind=engine)` on application startup. No Alembic setup yet.

## Security Rules
- Never expose API keys or internal database paths in frontend JS.
- Validate all file uploads in the backend (check MIME type and enforce a reasonable size limit, e.g., 5MB).
- Sanitize all user inputs before displaying them in HTML to prevent XSS (use `textContent` instead of `innerHTML` in JS).
- Ensure no sensitive PII (Personally Identifiable Information) or API keys are written to standard application logs.

## Testing
- Test API endpoints via the built-in Swagger UI: `http://localhost:8000/docs`.
- If the frontend cannot reach the backend, immediately check CORS configuration in `backend/main.py`.
- Always verify the `.env` file has `OPENAI_API_KEY` set before debugging AI generation issues.

## Known Limitations (MVP)
- Email, WhatsApp, and SMS sending functionalities are simulated (mocked in the backend).
- No WebSockets; real-time notifications rely on manual page reloads or simple polling.
- The system is single-tenant (no multi-organization or multi-workspace support).
- Authentication is rudimentary (session-based or simple headers); there is no JWT implementation yet.

## Common Issues & Fixes
- **CORS Error**: Ensure backend starts on port 8000 and frontend on 5500. Check `CORSMiddleware` origins list in `main.py`.
- **Database Lock (`sqlite3.OperationalError`)**: Stop the backend, ensure no other processes are reading the `.db` file, and restart.
- **OpenAI Rate Limits**: Implement basic exponential backoff in `ai_service.py` or use mock responses during heavy local testing.
