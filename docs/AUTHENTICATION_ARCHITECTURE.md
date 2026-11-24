# Vivi Authentication Architecture

## Sessions

- Login creates an opaque cryptographically random session token.
- PostgreSQL stores only a SHA-256 hash of the token.
- The browser receives the raw token in an HttpOnly `VIVI_SESSION` cookie.
- Sessions expire after 14 days and are not extended automatically.
- Logout revokes the current session.
- Password reset and password change revoke all sessions.

## Passwords

- Password hashes use Argon2id with `argon2-cffi`.
- Passwords are validated independently on the backend.
- Successful login can rehash passwords whose parameters are outdated.

## Challenges

- Email verification and password reset tokens are cryptographically random.
- PostgreSQL stores only token hashes.
- Verification challenges expire after 24 hours.
- Reset challenges expire after one hour.
- Replaced challenges and consumed challenges are invalidated.

## Origin and CSRF protection

- Authentication mutations require `X-CSRF-Token`.
- The browser receives a `VIVI_CSRF` double-submit cookie.
- Trusted Origin and Referer values are enforced.
- CORS permits only explicitly configured origins.

## Database rate limiting

- Registration, login, resend, and reset actions use PostgreSQL counters.
- Counters use 15-minute windows by default.
- Limits are per action and request IP.
- The API returns HTTP 429 after a threshold is reached.
