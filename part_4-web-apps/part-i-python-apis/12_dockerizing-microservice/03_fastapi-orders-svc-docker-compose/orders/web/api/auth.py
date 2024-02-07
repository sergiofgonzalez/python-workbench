"""Orders Service Authorization module"""
from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate

public_key_text = (Path(__file__).parent / "../../../public_key").read_text()
public_key = load_pem_x509_certificate(
    public_key_text.encode("utf-8")
).public_key()


def decode_and_validate_token(access_token):
    """
    Validates an access token. If the token is valid, its payload will be
    returned as a dict object. Otherwise, an exception will be raised.
    """
    return jwt.decode(
        access_token,
        key=public_key,  # type: ignore
        algorithms=["RS256"],
        audience=[
            "http://localhost:8080/orders",
            "http://127.0.0.1:8080/orders",
        ],
    )
