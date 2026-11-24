# Vivi Local Development

## Supported runtimes

- Node.js 24 LTS-compatible with the pinned Next.js dependency
- pnpm 10
- Python 3.12 or 3.13
- uv
- PostgreSQL 16 or 17

Docker is optional. The compose file provides PostgreSQL 17 and requires `POSTGRES_PASSWORD` in the root `.env`.

## Frontend

```powershell
cd frontend
pnpm install
pnpm dev
pnpm lint
pnpm test
pnpm build
```

The frontend runs at `http://localhost:3000`.

## Backend

```powershell
cd backend
Copy-Item .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

The backend runs at `http://127.0.0.1:8000`.

Health endpoints:

- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`

## PostgreSQL alternatives

### Docker Compose

Create a root `.env` containing `POSTGRES_PASSWORD`, then run:

```powershell
docker compose up -d postgres
```

Set `DATABASE_URL` in `backend/.env` to the matching database user and password.

### Native PostgreSQL

Install PostgreSQL 16 or 17, create a database named `vivi`, and set `DATABASE_URL` using the `postgresql+psycopg://` scheme.

The current development environment uses an existing PostgreSQL 18 service because PostgreSQL 17 could not be completed reliably. PostgreSQL 18 is local-only and is not the deployment baseline.

## Alembic

From `backend`:

```powershell
uv run alembic upgrade head
uv run alembic downgrade base
uv run alembic upgrade head
```

Never commit `.env` files or database credentials.
