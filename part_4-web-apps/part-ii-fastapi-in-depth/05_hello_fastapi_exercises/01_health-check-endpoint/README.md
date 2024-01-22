# Exercise 01: Health-check endpoint
> illustrates how to create a health-check endpoint using FastAPI

## Description

This application exposes an endpoint `GET /health-check` that returns a health check signal that includes the current timestamp in UTC format.

### Starting the project

You can start the project with:

```bash
uvicorn fastapi-svc.web:app --port 8080 --reload
```

### Testing the projects

You can test the endpoint with HTTPie:

```bash
$ http localhost:8080/health-check -v
GET /health-check HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 60
content-type: application/json
date: Mon, 22 Jan 2024 07:48:58 GMT
server: uvicorn

{
    "status": "OK",
    "utc_timestamp": "2024-01-22T07:48:59.026062"
}
```

Or using `requests` and Python's REPL:

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/health-check")
>>> r.json()
{'utc_timestamp': '2024-01-22T07:51:02.552294', 'status': 'OK'}
>>> r.status_code
200
```