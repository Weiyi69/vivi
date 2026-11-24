# Vivi Backend

The backend requires Python 3.12 or 3.13.

```powershell
Copy-Item .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
uv run pytest
uv run alembic upgrade head
uv run alembic downgrade base
```