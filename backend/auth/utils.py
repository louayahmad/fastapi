import random

import bcrypt


def hash_password(password: str) -> str:
    """Hash a password."""

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hashed version."""

    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def generate_random_number() -> int:
    """Generate a 6-digit identifier."""

    return random.randint(10**5, (10**6) - 1)
