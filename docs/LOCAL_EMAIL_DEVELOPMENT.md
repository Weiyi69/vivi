# Vivi Local Email Development

Set `EMAIL_MODE=development` and optionally `DEVELOPMENT_OUTBOX_DIR`.

Generated messages are written to a private local outbox. The default directory is excluded from Git. The outbox must never be enabled in production or exposed through a public route.

Outbox files contain recipient, subject, and verification/reset links. Raw challenge values must not be committed or logged.
