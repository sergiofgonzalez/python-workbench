# FastAPI *hello, world!* app
> introducing header parameters

## Description

A simple FastAPI app exposing a `GET /hi` endpoint that accepts a header parameter named `who` with the name.

Additionally, a `GET /agent` endpoint that returns the user-agent is defined.


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint

You can use HTTPie:

```bash
$ http localhost:8080/hi who:alexx --verbose
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2
who: alexx



HTTP/1.1 200 OK
content-length: 15
content-type: application/json
date: Thu, 18 Jan 2024 16:48:28 GMT
server: uvicorn

"Hello, alexx!"

```

The other endpoint can be tested in a similar way:

```bash
$ http localhost:8080/agent --verbose
GET /agent HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 26
content-type: application/json
date: Thu, 18 Jan 2024 16:51:22 GMT
server: uvicorn

"User-Agent: HTTPie/3.2.2"
```

### Testing the endpoint with `requests`

In the `requests` package, the body is provided as a parameter:

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi", headers={"who":"alexx"})
>>> r.json()
'Hello, alexx!'
>>> r = requests.get("http://localhost:8080/agent")
>>> r.json()
'User-Agent: python-requests/2.31.0'
>>>
```
