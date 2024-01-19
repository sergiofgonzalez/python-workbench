# FastAPI *hello, world!* app
> injecting a custom header in the response

## Description

A simple FastAPI app exposing a `GET /header/{name}/{value}` endpoint that injects a custom HTTP header named `name` with the given `value`


```bash
$ poetry install

$ poetry run uvicorn hello.main:app --port 8080 --reload
```

### Testing the endpoint with HTTPie


```bash
$ http localhost:8080/header/x-my-header/my-value
HTTP/1.1 200 OK
content-length: 39
content-type: application/json
date: Fri, 19 Jan 2024 11:23:19 GMT
server: uvicorn
x-my-header: my-value

"header x-my-header has been injected!"

```

## Testing the endpoint with `requests`

```python
>>> import requests
exit>>> r = requests.get("http://localhost:8080/header/x-my-header/my-value")
>>> r.headers
{'date': 'Fri, 19 Jan 2024 11:26:27 GMT', 'server': 'uvicorn', 'content-length': '39', 'content-type': 'application/json', 'x-my-header': 'my-value'}
>>>
```
