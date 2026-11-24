# Vivi Testing Strategy

Status: planning

## Backend

- Pytest unit tests
- FastAPI API tests
- PostgreSQL integration tests
- Authentication and authorization tests
- Processing tests
- Provider and unavailable-service tests
- Worker retry and failure tests

## Frontend

- Vitest unit/component tests
- React Testing Library interaction tests
- Zod and form validation tests
- Responsive checks

## End-to-end

- Registration and login
- Class and study-kit lifecycle
- Material upload and processing
- Study guide, flashcards, practice tests
- Smart Study
- Analytics
- Account deletion

## Quality gates

No implementation phase is complete until relevant tests pass, lint/type checks pass, migrations are verified where applicable, and no secrets or generated artifacts are in the diff.
