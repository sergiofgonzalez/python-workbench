# FastAPI *hello, world!* app
> returning a custom status code

## Description

A simple FastAPI app exposing a `GET /happy` endpoint that returns a custom status code.


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint with HTTPie


```bash
$ http localhost:8080/happy -v
GET /happy HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 6
content-type: application/json
date: Fri, 19 Jan 2024 11:11:39 GMT
server: uvicorn

"😀"
```

## Testing the endpoint with `requests`

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/happy")
>>> r.status_code
202
>>>
```
