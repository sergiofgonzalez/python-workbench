# FastAPI *hello, world!* app
> introducing path parameters

## Description

A simple FastAPI app exposing a `GET /hi/{who}` endpoint that returns a greeting message.


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint

You can use HTTPie:

```bash
(hello-py3.10) $ http "localhost:8080/hi/jason isaacs" --verbose
GET /hi/Jason%20Isaacs HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 22
content-type: application/json
date: Thu, 18 Jan 2024 16:04:29 GMT
server: uvicorn

"Hello, jason isaacs!"

```