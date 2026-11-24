# Vivi

Vivi is a planned, self-hostable, AI-powered learning platform for organizing classes and study kits, processing learning materials, generating study resources, and tracking demonstrated mastery.

## Planning status

The repository is in **Phase 1 implementation verification**. The foundation builds and the backend health/migration checks have been executed.

The initial Phase 0 planning commit is on `main` and was pushed to GitHub.

## Repository baseline

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI, Pydantic, SQLAlchemy 2.x, Alembic
- Database: PostgreSQL
- AI: provider contract only; no model or paid API
- Storage: local-storage contract only
- Package managers: pnpm and uv

## Local environment observed

- Windows 11, 16 GB RAM
- Intel i5-10300H, 8 logical processors
- NVIDIA RTX 2060 with 6 GB VRAM
- 206 GB free on C:, 760 GB free on D:
- Node.js 24.14.0
- pnpm 10.34.9
- Python 3.12.15 via uv
- uv 0.13.1
- Git 2.53.0
- Docker and Ollama are not installed
- PostgreSQL is available locally for development

## Documentation

- [Product Requirements](docs/PRD.md)
- [Roadmap](docs/ROADMAP.md)
- [Features](docs/FEATURES.md)
- [User Flows](docs/USER_FLOWS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Database Design](docs/DATABASE_DESIGN.md)
- [API Design](docs/API_DESIGN.md)
- [Design System](docs/DESIGN_SYSTEM.md)
- [Security](docs/SECURITY.md)
- [Free Infrastructure Strategy](docs/FREE_INFRASTRUCTURE_STRATEGY.md)
- [Testing Strategy](docs/TESTING_STRATEGY.md)
- [Decisions](docs/DECISIONS.md)
- [Phase 1 Readiness and Audit](docs/PHASE_1_READINESS.md)
- [Local Development](docs/LOCAL_DEVELOPMENT.md)
- [Backup and Restoration](docs/BACKUP_RESTORE.md)

## License and zero-cost scope

The implementation will favor permissively licensed open-source dependencies and will not require a commercial AI API or hosted service. Hardware, electricity, bandwidth, domain costs, and data backups remain real operating costs.
