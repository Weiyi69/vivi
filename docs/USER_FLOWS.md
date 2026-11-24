# Vivi User Flows

Status: planning

## Account

1. Student registers.
2. Student logs in with a server-side session.
3. Protected resources are authorized by the backend.
4. Logout revokes the session; account deletion removes private data according to the deletion policy.

## Study organization

1. Student creates a class.
2. Student creates a study kit in the class.
3. Student opens the kit workspace.
4. Student switches between Materials, Smart Study, Study Guide, Flashcards, and Test.

## Material processing

1. Student adds a material.
2. Backend validates format, size, ownership, and content.
3. Worker extracts, normalizes, and segments text.
4. Embeddings are generated locally when available.
5. UI displays pending, processing, ready, or failed status.
6. A failed job exposes safe recovery actions.

## Learning tools

All generated tools resolve the selected kit and only its authorized materials as primary context. The UI distinguishes source-grounded material from generated interpretation.
