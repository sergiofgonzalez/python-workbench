# Exercise 03: Query parameter management
> illustrates how to manage query parameters in an endpoint using FastAPI

## Description

This application exposes an endpoint `GET /hi/who={who}` that returns the following JSON string `"Hello? {who}?"`.

### Starting the project

You can start the project with:

```bash
uvicorn fastapi-svc.web:app --port 8080 --reload
```

### Testing the projects

You can test the endpoint with HTTPie:

```bash
$ http localhost:8080/hi who==sergio -v
GET /hi?who=sergio HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 16
content-type: application/json
date: Mon, 22 Jan 2024 08:24:36 GMT
server: uvicorn

"Hello? sergio?"
```

The `GET /hi/` endpoint should return a `"422 Unprocessable Entity"`:

| NOTE: |
| :---- |
| A `422 (Unprocessable Entity)` should be sent when sending a malformed payload that is syntactically correct, but missing a required parameters, or containing an invalid parameter, or assigning a wrong value or type to a parameter. |


```bash
$ http localhost:8080/hi -v
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 422 Unprocessable Entity
content-length: 139
content-type: application/json
date: Mon, 22 Jan 2024 08:25:49 GMT
server: uvicorn

{
    "detail": [
        {
            "input": null,
            "loc": [
                "query",
                "who"
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.5/v/missing"
        }
    ]
}
```

Or using `requests` and Python's REPL:

You can format the query string in the URL:

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi?who=sergio")
>>> r.status_code
200
>>> r.json()
'Hello? sergio?'
```

or using a separate object:

```python
>>> import requests
>>> query_params = {"who": "sergio"}
>>> r = requests.get("http://localhost:8080/hi", params=query_params)
>>> r.status_code
200
>>> r.json()
'Hello? sergio?'
```


or for the unhappy path:

```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi")
>>> r.status_code
422
```