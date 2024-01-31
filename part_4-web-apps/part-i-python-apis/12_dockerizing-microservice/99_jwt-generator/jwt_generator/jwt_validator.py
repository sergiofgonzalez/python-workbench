"""Validates a specific JWT"""
from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate

public_key_cert_contents = Path("public_key").read_text()
public_key = load_pem_x509_certificate(
    public_key_cert_contents.encode("utf-8")
).public_key()

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguY29mZmVlbWVzaC5pby8iLCJzdWIiOiJlYzdiYmNjZi1jYTg5LTRhZjMtODJhYy1iNDFlNDgzMWE5NjIiLCJhdWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwODAvb3JkZXJzIiwiaWF0IjoxNzA2MDI0MDAzLCJleHAiOjE3MDYxMTA0MDMsInNjb3BlIjoib3BlbmlkIn0.C5tt5eivJJcC2K1ura0RAig_X3pbfuJi7bBddlCUJKRGVeygLhdPyQ5mnvaIhAbAo7uxLWj_EMOJjNgROYCKUuQ6JnyEr7fySOGTOwoCAkRoH6HxGmL15CAm5YNIR0q1RUBprs5ZyvO5LxaRhtq7lmbdxYzotMLXYccoC1szSc2EdFzkHbQoVUnfof4-1R558SxZ09sM9FdHaeXmGskomlwg--LTa_PMuUTAUtBkKJEduMIEqVXBjD0zMPKUc2--wsKaKUayzvgpE6yu8Vte_0qusoXsTP162-741UA-ZbzW1pXQlqiKR30Eu5fOM0JDwQb4U5Ig5uqYlVe-y80ojh"  # pylint: disable=C0301:line-too-long

print(jwt.decode(
    access_token,
    key=public_key,  # type: ignore
    algorithms=["RS256"],
    audience=["http://127.0.0.1:8080/orders"],
))
