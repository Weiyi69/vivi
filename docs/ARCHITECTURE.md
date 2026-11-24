# Vivi Architecture

Status: Phase 1 implementation

## Baseline

Vivi will use a monorepo with separate Next.js frontend and FastAPI backend.

```text
frontend/        Next.js application
backend/         FastAPI application, migrations, worker
infrastructure/  Docker, Caddy, operational configuration
docs/            Product and engineering documentation
scripts/         Developer and release scripts
.github/         CI workflows
```

## Runtime components

- Next.js server and browser client
- FastAPI API
- PostgreSQL primary database
- pgvector extension
- Dedicated Python worker
- Ollama for optional local generation
- Sentence Transformers or an ONNX-compatible local embedding provider
- Local filesystem storage behind a storage interface
- Caddy reverse proxy for self-hosted deployment

Docker is optional and was not available during Phase 1 verification. The compose file uses PostgreSQL 17 and is not required for native local development.

## Backend boundaries

- API routes perform authentication and HTTP concerns
- Pydantic schemas validate boundaries
- Services implement reusable domain behavior
- Repositories own persistence
- AI providers implement a shared interface
- Workers call processing services asynchronously

## AI boundary

The frontend must never receive model credentials or call inference endpoints directly. The backend owns provider selection and retrieval. The provider interface allows Ollama, a future local provider, or a graceful unavailable state.

## Background jobs

The initial queue is PostgreSQL-backed. Jobs are claimed by transaction-safe row locking or `FOR UPDATE SKIP LOCKED`. No Redis or Celery dependency will be introduced unless measured load demonstrates a need.

## Observability and operations

- Health endpoints distinguish process liveness from dependency readiness.
- Structured JSON logs include timestamp, level, request/correlation ID, route, and safe error code.
- Logs must not contain passwords, cookies, authorization headers, document contents, or unredacted model prompts.
- Database migrations must be forward-reviewed and reversible through a documented downgrade only where safe.
- Backups cover PostgreSQL, uploaded files, configuration, and model inventory separately.
