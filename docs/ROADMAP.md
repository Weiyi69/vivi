# Vivi Development Roadmap

Status: planning

## Phase 0: Product discovery

Status: in progress

- Prepare PRD and feature inventory
- Confirm local and remote repository state
- Record unresolved requirements
- Acceptance: approved scope and phase plan

## Phase 1: Foundation

- Initialize monorepo structure
- Establish frontend, backend, database, migrations, and test infrastructure
- Add core configuration and Docker Compose
- Acceptance: documented baseline builds and tests start successfully

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
