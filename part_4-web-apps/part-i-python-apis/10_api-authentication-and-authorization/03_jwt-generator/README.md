# JWT generator
> generates an RS256 signed JWT

## Description

Simple example that illustrates how to generate an RSA based JWT using Python.

Before running the program, you have to generate a public/private key pair using OpenSSL:

```bash
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout private_key.pem \
  -out public_key \
  -subj "/CN=coffeemesh"
```

Then you can generate a token using:

```bash
$ poetry run python jwt_generator/jwt_generator.py
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.[...].xw-9O[...]MA
```

