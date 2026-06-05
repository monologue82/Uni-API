import base64
import os

from cryptography.fernet import Fernet


def _get_cipher() -> Fernet:
    raw_key = (
        os.environ.get("UNIAPI_ENCRYPT_KEY", "")
        or "dW5pLWFwaS1kZWZhdWx0LWtleS1mb3ItZGV2LXVzZQ=="
    )
    key = base64.urlsafe_b64encode(raw_key.encode().ljust(32, b"\x00")[:32])
    return Fernet(key)


_cipher = _get_cipher()


def encrypt(plain_text: str) -> str:
    if not plain_text:
        return ""
    return _cipher.encrypt(plain_text.encode()).decode()


def decrypt(cipher_text: str) -> str:
    if not cipher_text:
        return ""
    return _cipher.decrypt(cipher_text.encode()).decode()
