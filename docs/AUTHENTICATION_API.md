# Vivi Authentication API

All routes are below `/api/v1`.

| Method | Path | Purpose |
|---|---|---|
| GET | `/auth/csrf` | Obtain a CSRF token |
| POST | `/auth/register` | Register an unverified account |
| POST | `/auth/login` | Create a server-side session |
| POST | `/auth/logout` | Revoke the current session |
| POST | `/auth/verify-email` | Verify an account |
| POST | `/auth/resend-verification` | Rotate and resend verification |
| POST | `/auth/password-reset/request` | Request a reset challenge |
| POST | `/auth/password-reset/confirm` | Set a password and revoke sessions |
| GET | `/auth/me` | Retrieve the current profile |
| PATCH | `/auth/me` | Update display name |
| POST | `/auth/change-password` | Change password and revoke sessions |

Protected operations derive identity from the session cookie. Frontend-supplied user IDs are never authorization proof.

Registration and reset responses use generic messages to prevent account enumeration.
