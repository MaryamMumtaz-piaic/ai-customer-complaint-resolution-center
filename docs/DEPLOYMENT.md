# Deployment Guide

This guide covers how to deploy ComplaintIQ from local development to a production server.

## Local Development Setup
See the `README.md` for standard local setup using `uvicorn` and Python HTTP server.

## Docker Deployment (Recommended)

To deploy using Docker, create a `docker-compose.yml` in the project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=sqlite:///./data/complaint_center.db
    volumes:
      - ./data:/app/data
      - ./backend/uploads:/app/uploads

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
```

**Steps to run:**
1. Populate your `.env` file in the root directory.
2. Run `docker-compose up -d --build`.
3. The frontend is accessible at `http://localhost`, the API at `http://localhost:8000`.

## Production Deployment (Ubuntu VPS)

1. **Provision Server**: Ubuntu 22.04 LTS recommended.
2. **Install Dependencies**: `sudo apt update && sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx`
3. **Backend Setup**:
   - Clone repo, setup `venv`, install requirements.
   - Run backend using `gunicorn` with `uvicorn` workers:
     `gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000 --daemon`
   - Set up a systemd service to manage the Gunicorn process.
4. **Nginx Configuration**:
   Create `/etc/nginx/sites-available/complaintiq`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           root /path/to/complaintiq/frontend;
           index index.html;
           try_files $uri $uri/ /index.html;
       }

       location /api/ {
           proxy_pass http://127.0.0.1:8000/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
5. **SSL Setup**:
   `sudo certbot --nginx -d yourdomain.com`

## Environment Variables Reference
Ensure these are set securely in production:
- `OPENAI_API_KEY`: Required.
- `SECRET_KEY`: Long, random string for security.
- `CORS_ORIGINS`: Comma-separated list of allowed domains (e.g., `https://yourdomain.com`).

## Monitoring Suggestions
- Use **Sentry** for Python error tracking.
- Monitor OpenAI API usage via the OpenAI dashboard to control costs.
- Use **Prometheus/Grafana** to monitor server CPU/RAM, especially during vector ingestion.
