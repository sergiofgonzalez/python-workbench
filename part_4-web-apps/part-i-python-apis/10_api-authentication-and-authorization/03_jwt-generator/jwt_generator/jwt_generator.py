"""Simple program that generates an RSA256 signed JWT"""
from datetime import datetime, timedelta
from pathlib import Path
from math import floor

import jwt
from cryptography.hazmat.primitives import serialization


def generate_rsa_signed_jwt():
    now = datetime.utcnow()
    payload = {
        "iss": "https://auth.coffeemesh.io/",
        "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a999",
        "aud": "http://127.0.0.1:8080/orders",
        "iat": floor(now.timestamp()),
        "exp": floor((now + timedelta(hours=24)).timestamp()),
        "scope": "openid",
    }
    private_key_contents = Path("private_key.pem").read_text(encoding="utf-8")
    private_key = serialization.load_pem_private_key(
        private_key_contents.encode(),
        password=None,
    )
    return jwt.encode(
        payload=payload, key=private_key, algorithm="RS256"  # type: ignore
    )


if __name__ == "__main__":
    print(generate_rsa_signed_jwt())
