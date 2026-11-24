# Vivi API Design

Status: planning

## Conventions

- JSON REST API under `/api/v1`
- FastAPI Pydantic request and response schemas
- Server-side secure sessions with HttpOnly cookies
- Backend authorization on every protected operation
- Stable error envelope
- Cursor or keyset pagination for large collections

## Initial route groups

- `/api/v1/auth`
- `/api/v1/account`
- `/api/v1/classes`
- `/api/v1/study-kits`
- `/api/v1/materials`
- `/api/v1/jobs`
- `/api/v1/study-guides`
- `/api/v1/flashcards`
- `/api/v1/practice-tests`
- `/api/v1/smart-study`
- `/api/v1/analytics`

## Security requirements

- CSRF protection for cookie-authenticated mutations
- Strict file type and size validation
- Signed or server-resolved file access
- Rate limiting on auth and AI endpoints
- No sensitive model endpoint exposure
- Safe, non-sensitive error messages
