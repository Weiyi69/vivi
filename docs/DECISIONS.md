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

## Resolved planning recommendations

1. Python minimum: Python 3.12; allow 3.12 and 3.13 initially, managed by uv. Python 3.14 is not the support floor because many scientific/document dependencies may lag it.
2. Node baseline: use the environment's Node 24 LTS baseline where its Next.js release is compatible; otherwise pin the newest compatible LTS. Do not add a new runtime until dependency compatibility is confirmed.
3. Initial language model: benchmark Qwen3-4B-Instruct-2507 as the preferred candidate, with Qwen2.5-1.5B-Instruct as the fallback.
4. Initial embedding model: benchmark multilingual-e5-base at 768 dimensions, not BGE-M3, for the first retrieval implementation.
5. Email: use optional configurable SMTP; do not add a paid provider dependency. Development must not expose reset links outside the server. Product should clearly indicate when verification or reset delivery is unavailable.
6. YouTube: MVP accepts manual transcripts/notes and can store metadata after explicit user link submission. Automatic extraction is deferred pending terms and implementation review.
7. Combining: create same-owner material snapshot/link records with preserved source attribution. Do not duplicate uploaded files.
8. Catalog: administrator-owned, licensed or public-domain content only, with provenance and moderation fields. Student sharing and public catalog submission are deferred.

## Pending approval

1. Final Phase 1 architecture and dependency plan.
2. The exact local model revisions after benchmark validation.
3. Production SMTP transport selection.
4. YouTube extraction implementation scope.
5. Whether source snapshots should retain extracted text after original kit deletion.
