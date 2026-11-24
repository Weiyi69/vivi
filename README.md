# Vivi

Vivi is a planned, self-hostable, AI-powered learning platform for organizing classes and study kits, processing learning materials, generating study resources, and tracking demonstrated mastery.

## Planning status

The repository is currently in **Phase 0 / Phase 1 planning preparation**. No application implementation is complete.

The GitHub remote is empty. The local workspace has no existing source files or Git history.

## Repository baseline

- Frontend planned: Next.js, React, TypeScript, Tailwind CSS
- Backend planned: FastAPI, Pydantic, SQLAlchemy 2.x, Alembic
- Database planned: PostgreSQL with pgvector
- AI planned: Ollama plus a replaceable provider interface
- Storage planned: local filesystem behind a storage abstraction
- Package managers: pnpm and uv

## Local environment observed

- Windows 11, 16 GB RAM
- Intel i5-10300H, 8 logical processors
- NVIDIA RTX 2060 with 6 GB VRAM
- 206 GB free on C:, 760 GB free on D:
- Node.js 24.14.0
- pnpm 10.34.9
- Python 3.14.10
- uv 0.13.1
- Git 2.53.0
- Docker, Ollama, PostgreSQL, and pgvector are not currently installed

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

## License and zero-cost scope

The implementation will favor permissively licensed open-source dependencies and will not require a commercial AI API or hosted service. Hardware, electricity, bandwidth, domain costs, and data backups remain real operating costs.
