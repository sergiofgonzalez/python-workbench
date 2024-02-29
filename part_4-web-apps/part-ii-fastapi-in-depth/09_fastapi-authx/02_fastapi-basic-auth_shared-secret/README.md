# FastAPI server with basic authentication

This project illustrates how to enable Basic Auth scheme on a FastAPI web application, and how to use a simple shared secret to authenticate requests. The client should sent the shared secret in the `Authorization` HTTP header.


## Setting up shop

The project uses Poetry. To set things up type:

```bash
poetry install
```

## Running the application

To run the application in development mode type:

```bash
poetry run python securebasic/server.py
```

This will start the server in port 8080 with reloading enabled.

You can also run the application with `uvicorn`:

```bash
poetry run uvicorn securebasic.server:app \
  --port 8080 \
  --reload
```

## Testing the application

### Using HTTPie

```bash
# Unauthenticated request
$ http localhost:8080/who
HTTP/1.1 401 Unauthorized
content-length: 30
content-type: application/json
date: Thu, 15 Feb 2024 09:03:54 GMT
server: uvicorn
www-authenticate: Basic

{
    "detail": "Not authenticated"
}
```

```bash
# Authenticated request with incorrect username/password
$ http localhost:8080/who -a jason.isaacs:secret
HTTP/1.1 401 Unauthorized
content-length: 39
content-type: application/json
date: Thu, 15 Feb 2024 09:32:58 GMT
server: uvicorn

{
    "detail": "Incorrent user or password"
}
```

```bash
# Authenticated request with correct username and password
$ http localhost:8080/who -a bill.harford:fidelio
HTTP/1.1 200 OK
content-length: 48
content-type: application/json
date: Thu, 15 Feb 2024 09:33:27 GMT
server: uvicorn

{
    "password": "fidelio",
    "username": "bill.harford"
}
```

