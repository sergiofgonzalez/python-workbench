# FastAPI *hello, world!* app
> customizing the response types

## Description

A simple FastAPI app exposing a set of endpoints `/html`, `/plain`, `/xml` to illustrate how to customize the response type.


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint with HTTPie


```bash
 http localhost:8080/plain -v
GET /plain HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 6
content-type: text/plain; charset=utf-8
date: Fri, 19 Jan 2024 11:36:39 GMT
server: uvicorn

Hello!
```