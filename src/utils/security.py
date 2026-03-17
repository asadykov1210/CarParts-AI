import hashlib


def hash_password(password: str) -> str:
    # Хешируем пароль через SHA-256.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    # Проверяем совпадение пароля с хешем
    return hash_password(password) == password_hash
