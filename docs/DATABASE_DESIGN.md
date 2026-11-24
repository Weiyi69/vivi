# Vivi Database Design

Status: planning

## Core entities

Authentication entities include `users`, `user_sessions`, `email_verification_tokens`, `password_reset_tokens`, and `authentication_rate_limits`.

- users
- sessions
- classes
- study_kits
- materials
- material_versions or source records
- content_segments
- embeddings
- study_guides
- flashcard_decks and flashcards
- flashcard_reviews
- practice_tests and test_questions
- test_attempts and test_answers
- study_sessions and study_turns
- topic_knowledge snapshots
- background_jobs

## Ownership model

Private resources must have authorization derivable through an explicit owner or a parent owned by the user. Study kits belong to a class and owner. A material belongs to a kit unless future combining rules explicitly create a same-owner reference or snapshot model.

Every write and read of child records must verify the owner by joining through the ownership chain. A child table should not be trusted solely because it has a `user_id` copy or because the frontend supplied an owner value.

## Initial relationships

- User 1:N Classes
- Class 1:N Study Kits
- Study Kit 1:N Materials
- Study Kit 1:N Study Guides
- Study Kit 1:N Flashcard Decks
- Study Kit 1:N Practice Tests
- Study Kit 1:N Study Sessions
- Material 1:N Segments
- Segment 1:N Embeddings
- Flashcard 1:N Reviews
- Test Attempt 1:N Answers

## Deletion and archival rules

- Class deletion requires confirmation and explicit policy for child kits.
- Kit deletion removes kit-owned generated resources.
- Shared/reference materials are prohibited until ownership semantics are designed.
- Account deletion removes private data and stored files or schedules verified secure removal.

## pgvector

Embeddings use a dimension fixed to the selected embedding model. Retrieval must include owner and kit filters in the query, not only as application post-processing.
