# Vivi Development Roadmap

Status: planning

## Phase 0: Product discovery

Status: complete and published

- Prepare PRD and feature inventory
- Confirm local and remote repository state
- Record unresolved requirements
- Acceptance: repository baseline, scope, architecture, and free-cost assumptions documented

## Phase 1: Foundation

Status: implementation complete, final verification in progress

- Initialize monorepo structure
- Establish frontend, backend, database, migrations, and test infrastructure
- Add core configuration and Docker Compose
- Acceptance: documented baseline builds and tests start successfully

See [Phase 1 Readiness](PHASE_1_READINESS.md) for the detailed implementation plan and approval gate.

## Phase 2: Authentication

- Registration, login, logout, secure sessions
- Argon2id password hashing and CSRF protection
- Account deletion
- Acceptance: unauthorized access tests pass

## Phase 3: Dashboard and organization

- Classes, study kits, search, and workspace
- Acceptance: full user ownership and class/kit lifecycle tests pass

## Phase 4: Materials

- Upload, paste, YouTube policy, combine, describe, and catalog foundations
- Acceptance: validation, extraction, and ownership tests pass

## Phase 5: Processing and retrieval

- Worker, normalization, segmentation, embeddings, pgvector retrieval
- Acceptance: retry, failure, and source-attribution tests pass

## Phase 6: Study guides

## Phase 7: Flashcards

## Phase 8: Practice tests

## Phase 9: Smart Study

## Phase 10: Analytics

## Phase 11: Production release

Each implementation phase requires tests, documentation, security review, a Conventional Commit, and push verification.
