# Vivi Backup and Restoration

## Backup scope

Backups must cover:

- PostgreSQL database contents
- Uploaded files and private learning materials
- Application configuration templates
- Model and embedding inventory
- Deployment and TLS configuration

Database dumps alone do not recover uploaded documents. File backups alone do not recover database ownership metadata.

## PostgreSQL

Before any destructive operation, create a PostgreSQL dump outside the repository:

```powershell
pg_dump -h 127.0.0.1 -p 5432 -U postgres -d vivi --format=custom --file=backups/vivi.dump
```

Restore into an empty database:

```powershell
createdb -h 127.0.0.1 -p 5432 -U postgres vivi_restore
pg_restore -h 127.0.0.1 -p 5432 -U postgres -d vivi_restore --clean --if-exists backups/vivi.dump
```

Always verify restored row counts and application readiness before switching production traffic.

## Local files

Copy the configured storage directory to a separate physical or encrypted location. Do not publish uploaded content in Git, CI logs, or public web directories.

## Verification

Quarterly or before major migrations:

1. Restore a backup to a disposable database.
2. Restore a representative file snapshot.
3. Run migration and health checks.
4. Test read authorization against restored records.
5. Record the test date and restore result.

This document establishes an operating requirement; automated backup scheduling is not implemented in Phase 1.
