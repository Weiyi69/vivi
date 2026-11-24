import hashlib
import hmac
import re
import secrets
from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password_hasher = PasswordHasher(memory_cost=65536, time_cost=3, parallelism=2)


def normalize_email(email: str) -> str:
    local, separator, domain = email.strip().lower().rpartition("@")
    if not separator:
        return email.strip().lower()
    return f"{local}@{domain}".strip()


def validate_display_name(name: str) -> str:
    cleaned = " ".join(name.split())
    if len(cleaned) < 2 or len(cleaned) > 80:
        raise ValueError("Display name must contain 2 to 80 characters")
    if re.search(r"[\x00-\x1F\x7F]", cleaned):
        raise ValueError("Display name contains unsupported characters")
    return cleaned


def validate_password(password: str) -> None:
    if len(password) < 12 or len(password) > 128:
        raise ValueError("Password must contain 12 to 128 characters")


def hash_password(password: str) -> str:
    validate_password(password)
    return password_hasher.hash(password)


def verify_password(encoded: str, password: str) -> bool:
    try:
        return password_hasher.verify(encoded, password)
    except VerifyMismatchError:
        return False


def password_needs_rehash(encoded: str) -> bool:
    return password_hasher.check_needs_rehash(encoded)


def random_challenge() -> str:
    return secrets.token_urlsafe(32)


def challenge_hash(challenge: str) -> str:
    return hashlib.sha256(challenge.encode("ascii")).hexdigest()


def secure_compare(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)


def utcnow() -> datetime:
    return datetime.now(UTC)


def future(hours: int) -> datetime:
    return utcnow() + timedelta(hours=hours)
