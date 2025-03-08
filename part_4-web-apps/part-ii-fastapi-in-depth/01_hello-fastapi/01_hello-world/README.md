# FastAPI *hello, world!* app

## Description

The simplest FastAPI app exposing a `GET /hi` endpoint that returns a hardcoded "Hello, world!" message.

This project is configured with Poetry.

```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

## Testing the endpoint

You can use:
+ the browser
+ HTTPie text web client
+ Requests sync web client package
+ HTTPX sync/async web client package

### Using the browser

Point your fave browser to http://localhost:8080/hi to see the following result:

![Hello in the browser](docs/pics/hello-browser.png)


### Using the HTTPie text web client

HTTPie is installed as a dev dependency.

```bash
$ poetry run http localhost:8080/hi
HTTP/1.1 200 OK
content-length: 15
content-type: application/json
date: Thu, 18 Jan 2024 15:17:01 GMT
server: uvicorn

"Hello, world!"

```

You can use `-b` (==`--body`) to skip the response headers and print only the body:

```bash
$ poetry run http localhost:8080/hi --body
"Hello, world!"

```

And you can use `-v` (==`--verbose`) to print both the request headers, response headers and response body:

```bash
 poetry run http localhost:8080/hi --verbose
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 15
content-type: application/json
date: Thu, 18 Jan 2024 15:31:08 GMT
server: uvicorn

"Hello, world!"

```

### Using `requests`

You can use `requests` from the REPL:

```python
$ poetry run python
Python 3.10.13 (main, Jan 18 2024, 07:41:15) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> r = requests.get("http://localhost:8080/hi")
>>> r.json()
'Hello, world!'
>>>
```

### Using `httpx`

You can use `httpx` from the REPL:

```python
$ poetry run python
Python 3.10.13 (main, Jan 18 2024, 07:41:15) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import httpx
>>> r = httpx.get("http://localhost:8080/hi")
>>> r.json()
'Hello, world!'
>>>
```