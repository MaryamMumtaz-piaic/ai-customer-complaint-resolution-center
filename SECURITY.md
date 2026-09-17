# Security Policy

## Supported Versions

Currently, only the latest release of ComplaintIQ receives security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please DO NOT open a public issue.
Instead, send an email to the security team at `security@example.com` (placeholder).
We will review all reports and attempt to address valid vulnerabilities promptly.

## Security Best Practices for Deployment
- **HTTPS Only**: Ensure your production server uses TLS/SSL (e.g., via Let's Encrypt and Nginx).
- **Environment Variables**: Never commit `.env` files. Ensure `SECRET_KEY` is cryptographically strong and unique in production.
- **Database Security**: Restrict network access to the production PostgreSQL database.
- **Rate Limiting**: Implement rate limiting on API endpoints to prevent abuse (DDoS or OpenAI API quota exhaustion).

## Known Security Considerations for MVP
- **Authentication**: The current MVP utilizes basic/session auth. For enterprise use, implement OAuth2, JWT, or SAML.
- **Data Privacy**: Be cautious about the PII sent to the OpenAI API. Implement local sanitization of sensitive customer data before transmission if required by your compliance standards (e.g., GDPR, HIPAA).
- **Tenant Isolation**: The MVP is single-tenant. Do not host multiple distinct organizations on a single instance without implementing Row-Level Security (RLS) or database isolation.
