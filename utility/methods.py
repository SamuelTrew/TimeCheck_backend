import secrets


def generate_key(length: int) -> str:
    size = length * 3 // 4
    return secrets.token_urlsafe(size)
