# FastAPI *hello, world!* app
> introducing parameters in the body

## Description

A simple FastAPI app exposing a `POST /hi` endpoint that accepts a json such as:

```json
{
  "who": "your-name-here"
}
```


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint

You can use HTTPie:

```bash
$ http post localhost:8080/hi who=inma --verbose
POST /hi HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 15
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "who": "inma"
}


HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Thu, 18 Jan 2024 16:30:08 GMT
server: uvicorn

"Hello, inma!"
```

### Testing the endpoint with `requests`

In the `requests` package, the body is provided as a parameter:

```python
>> import requests
>>> r = requests.post("http://localhost:8080/hi", json={"who": "inma"})
>>> r.json()
'Hello, inma!'
```
