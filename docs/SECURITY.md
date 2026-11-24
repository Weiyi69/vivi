# Vivi Security

Status: planning

## Security baseline

- Argon2id password hashing
- Secure server-side sessions
- HttpOnly, SameSite, and appropriately secure cookies
- CSRF protection for cookie-authenticated mutations
- Backend ownership and authorization checks
- Pydantic and domain-level input validation
- Parameterized database access
- Strict file validation and allowlists
- Path traversal prevention
- Private file storage outside public web paths
- Rate limiting on authentication and resource-intensive endpoints
- Safe logging and secret redaction
- Account and file deletion controls

## Upload security

Validate extension, MIME type, size, and file parsing behavior. Store files using generated names. Never trust user-provided paths or frontend ownership fields.

## AI security

Keep model endpoints behind FastAPI. Retrieve only owner/kit-authorized segments. Treat model output as untrusted. Validate structured JSON before persistence or display.

## Dependency security

Pin dependencies, review licenses, run vulnerability scans where practical, and document known exceptions. No secrets or `.env` files are committed.
