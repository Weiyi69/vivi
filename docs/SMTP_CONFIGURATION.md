# Vivi SMTP Configuration

Set:

- `EMAIL_MODE=smtp`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM`
- `SMTP_USE_TLS`

Keep credentials outside source control. Production startup requires SMTP and secure cookies.

SMTP delivery failures return a safe 503 response. Self-hosted email requires a domain, DNS, server maintenance, TLS, and potentially IP reputation work. No free provider is guaranteed.
