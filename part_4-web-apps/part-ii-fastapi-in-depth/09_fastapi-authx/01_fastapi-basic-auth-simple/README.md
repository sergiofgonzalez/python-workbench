# FastAPI server with basic authentication

This project illustrates how to enable Basic Auth scheme on a FastAPI web application.


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
# Authenticated request
$ http -v -a bill.harford:fidelio localhost:8080/who
GET /who HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Basic YmlsbC5oYXJmb3JkOmZpZGVsaW8=
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 48
content-type: application/json
date: Thu, 15 Feb 2024 09:09:21 GMT
server: uvicorn

{
    "password": "fidelio",
    "username": "bill.harford"
}
```

### Using `requests` module

```python
# Unauthenticated requests
>>> import requests
>>> r = requests.get("http://localhost:8080/who")
>>> r.status_code
401
>>> r.json()
{'detail': 'Not authenticated'}
```

```python
# Authenticated requests
>>> import requests
>>> r = requests.get("http://localhost:8080/who", auth=("bill.hartford", "fidelio"))
>>> r.status_code
200
>>> r.json()
{'username': 'bill.hartford', 'password': 'fidelio'}
```
