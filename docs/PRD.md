# Vivi Product Requirements Document

Status: planning draft

## Vision

Vivi is an original, blue-and-white AI learning platform that converts a student's own learning materials into guided study experiences. It is not a document summarizer or generic chatbot.

## Product hierarchy

User Account -> Classes/Subjects -> Study Kits -> Materials and learning resources.

## Confirmed initial scope

- Secure account registration and login
- Classes and study kits
- PDF, DOCX, PPTX, and TXT materials
- Paste and described-study material sources
- Background processing and source-grounded retrieval
- Generated study guides
- Flashcards and spaced review
- Practice tests and attempts
- Context-aware AI tutor sessions
- Performance and topic-level progress

## Delivery exclusions for the first core release

- Paid plans or advertisements
- External paid AI requirements
- Collaborative sharing
- Audio/podcast generation
- Commercial catalog content
- Proprietary Thea branding or assets

## Core user stories

1. As a student, I can create a class and organize study kits.
2. As a student, I can upload or paste material and track processing.
3. As a student, I can generate a study guide with source references.
4. As a student, I can create, edit, and review flashcards.
5. As a student, I can take a generated practice test and review explanations.
6. As a student, I can ask a study-tutor questions within my selected kit.
7. As a student, I can see weak topics and receive review recommendations.
8. As a user, I can delete my account and associated private data.

## Acceptance principles

- Protected records require backend ownership and authorization checks.
- AI answers identify source coverage and limitations.
- Mastery requires demonstrated performance.
- Processing failures preserve a recoverable status and safe error detail.
- Core workflows operate with local AI unavailable only in degraded mode.

## Product decisions requiring approval

- Email verification implementation and password-reset delivery
- YouTube transcript retrieval policy
- Postgres-backed queue versus a future broker
- Initial local model size and context profile
