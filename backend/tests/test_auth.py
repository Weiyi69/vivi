from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app
from app.models.auth import PasswordResetToken, User, VerificationToken

client = TestClient(create_app())


def csrf_headers():
    csrf = client.get("/api/v1/auth/csrf")
    token = csrf.json()["csrf_token"]
    client.cookies.set("VIVI_CSRF", token)
    return {"X-CSRF-Token": token}


def test_register_verify_login_and_profile(clean_auth_tables):
    headers = csrf_headers()
    response = client.post(
        "/api/v1/auth/register",
        headers=headers,
        json={
            "display_name": "Vivi Student",
            "email": "Student@Example.com",
            "password": "correct-horse-battery",
            "password_confirmation": "correct-horse-battery",
        },
    )
    assert response.status_code == 202

    assert clean_auth_tables.query(VerificationToken).count() == 1
    user = clean_auth_tables.query(User).one()
    assert user.normalized_email == "student@example.com"
    assert user.password_hash != "correct-horse-battery"

    outbox = Path("tests/.test-outbox")
    message = next(outbox.glob("*.txt"))
    link_line = message.read_text(encoding="utf-8").split("token=", 1)[1].strip()
    verify = client.post(
        "/api/v1/auth/verify-email",
        headers=headers,
        json={"token": link_line},
    )
    assert verify.status_code == 200

    login = client.post(
        "/api/v1/auth/login",
        headers=headers,
        json={
            "email": "STUDENT@example.com",
            "password": "correct-horse-battery",
        },
    )
    assert login.status_code == 200
    profile = client.get("/api/v1/auth/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["display_name"] == "Vivi Student"


def test_duplicate_registration_has_generic_response(clean_auth_tables):
    headers = csrf_headers()
    payload = {
        "display_name": "First Student",
        "email": "first@example.com",
        "password": "correct-horse-battery",
        "password_confirmation": "correct-horse-battery",
    }
    assert (
        client.post("/api/v1/auth/register", headers=headers, json=payload).status_code
        == 202
    )
    assert (
        client.post("/api/v1/auth/register", headers=headers, json=payload).status_code
        == 202
    )
    assert clean_auth_tables.query(User).count() == 1


def test_password_reset_rotates_challenge_and_revokes_sessions(clean_auth_tables):
    headers = csrf_headers()
    register = client.post(
        "/api/v1/auth/register",
        headers=headers,
        json={
            "display_name": "Reset Student",
            "email": "reset@example.com",
            "password": "correct-horse-battery",
            "password_confirmation": "correct-horse-battery",
        },
    )
    assert register.status_code == 202

    user = clean_auth_tables.query(User).one()
    user.email_verified_at = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    )
    clean_auth_tables.commit()

    login = client.post(
        "/api/v1/auth/login",
        headers=headers,
        json={"email": "reset@example.com", "password": "correct-horse-battery"},
    )
    assert login.status_code == 200
    reset_request = client.post(
        "/api/v1/auth/password-reset/request",
        headers=headers,
        json={"email": "reset@example.com"},
    )
    assert reset_request.status_code == 200
    challenge = clean_auth_tables.query(PasswordResetToken).one()
    assert challenge.used_at is None
    outbox = Path("tests/.test-outbox")
    message = max(outbox.glob("*.txt"), key=lambda path: path.stat().st_mtime)
    raw_token = message.read_text(encoding="utf-8").split("token=", 1)[1].strip()
    confirm = client.post(
        "/api/v1/auth/password-reset/confirm",
        headers=headers,
        json={
            "token": raw_token,
            "password": "new-correct-horse-battery",
            "password_confirmation": "new-correct-horse-battery",
        },
    )
    assert confirm.status_code == 200
    profile = client.get("/api/v1/auth/me", headers=headers)
    assert profile.status_code == 401
