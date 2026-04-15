import secrets
import hashlib


def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()


def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    return hashlib.sha256(plain_secret.encode()).hexdigest() == hashed_secret


def generate_api_key() -> str:
    return "ak_" + secrets.token_hex(16)


def generate_api_secret() -> str:
    return "as_" + secrets.token_hex(16)