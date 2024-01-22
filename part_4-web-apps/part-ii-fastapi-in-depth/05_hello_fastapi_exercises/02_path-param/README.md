# Exercise 02: Path parameter management
> illustrates how to manage path parameters in an endpoint using FastAPI

## Description

This application exposes an endpoint `GET /hi/{who}` that returns the following JSON string `"Hello? {who}?"`.

### Starting the project

You can start the project with:

```bash
uvicorn fastapi-svc.web:app --port 8080 --reload
```

### Testing the projects

You can test the endpoint with HTTPie:

```bash
 http localhost:8080/hi/sergio -v
GET /hi/sergio HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 16
content-type: application/json
date: Mon, 22 Jan 2024 08:00:42 GMT
server: uvicorn

"Hello? sergio?"

```

The `GET /hi/` endpoint should return a `"404 Not Found"`:

```bash
$ http localhost:8080/hi/
HTTP/1.1 404 Not Found
content-length: 22
content-type: application/json
date: Mon, 22 Jan 2024 08:03:14 GMT
server: uvicorn

{
    "detail": "Not Found"
}
```

Or using `requests` and Python's REPL:

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi/sergio")
>>> r.json()
'Hello? sergio?'
>>> r.status_code
200
```

or for the unhappy path:

```python
$ python
Python 3.10.13 (main, Jan 18 2024, 07:41:15) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> r = requests.get("http://localhost:8080/hi")
>>> r.status_code
404
```