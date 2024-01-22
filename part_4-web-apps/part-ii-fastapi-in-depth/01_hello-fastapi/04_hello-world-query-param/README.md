# FastAPI *hello, world!* app
> introducing query parameters

## Description

A simple FastAPI app exposing a `GET /hi?who=<name>` endpoint that returns a greeting message.


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint

You can use HTTPie:

```bash
$ poetry run http localhost:8080/hi?who=sergio --verbose
GET /hi?who=sergio HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 16
content-type: application/json
date: Thu, 18 Jan 2024 16:09:51 GMT
server: uvicorn

"Hello, sergio!"

```

Note that our application fails with a "422 Unprocessable Entity" when we don't supply the query parameter.

### Testing the endpoint with `requests`

In the `requests` package, the parameters can be either provided directly in the URL:

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi?who=adri")
>>> r.json()
'Hello, adri!'
```

or through a separate params object:

```bash
>>> import requests
>>> params = { "who": "adri" }
>>> r = requests.get("http://localhost:8080/hi", params=params)
>>> r.json()
'Hello, adri!'
```