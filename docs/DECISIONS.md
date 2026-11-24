# Vivi Architectural Decisions

Status: planning

## Adopted

1. Use a monorepo with separate frontend and backend.
2. Use Next.js/React/TypeScript for the frontend.
3. Use FastAPI/Pydantic/SQLAlchemy/Alembic for the backend.
4. Use PostgreSQL and pgvector.
5. Use a PostgreSQL-backed queue initially.
6. Use an AI provider abstraction with Ollama as the initial local implementation.
7. Use local filesystem storage behind an abstraction.
8. Do not require Redis or Celery until measured requirements justify them.
9. Do not require commercial AI or hosted paid services.

## Pending approval

1. Python support floor; likely a maintained stable 3.12 or 3.13 rather than system Python 3.14.
2. Node LTS baseline.
3. Initial local generation model.
4. Initial embedding model and vector dimensions.
5. Email verification and password-reset delivery strategy.
6. YouTube transcript retrieval policy.
7. Material combining semantics.
8. Catalog licensing and moderation model.
