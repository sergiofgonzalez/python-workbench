# Exercise 04: Body Management
> illustrates how to manage endpoints that expect payloads in the body of the request using FastAPI

## Description

This application exposes an endpoint `GET /hi` that expects a body payload:

```json
{
    "who": "name"
}
```

and returns the following JSON string `"Hello? {who}?"`.


While sending a body in a GET request is a bit unorthodox, it's supported by FastAPI as can be seen in the example.

Because it's a weird thing to do, it's highly discouraged, and you should use a POST request when you're expecting a request body with the information.

### Starting the project

You can start the project with:

```bash
uvicorn fastapi-svc.web:app --port 8080 --reload
```

### Testing the projects

You can test the GET endpoint with HTTPie:

```bash
$ http get localhost:8080/hi who=sergio --verbose
GET /hi HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 17
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "who": "sergio"
}


HTTP/1.1 200 OK
content-length: 16
content-type: application/json
date: Mon, 22 Jan 2024 09:01:53 GMT
server: uvicorn

"Hello? sergio?"
```

The `GET /hi` endpoint should return a `"422 Unprocessable Entity"`:

| NOTE: |
| :---- |
| A `422 (Unprocessable Entity)` should be sent when sending a malformed payload that is syntactically correct, but missing a required parameters, or containing an invalid parameter, or assigning a wrong value or type to a parameter. |


```bash
$ http get localhost:8080/hi --verbose
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 422 Unprocessable Entity
content-length: 138
content-type: application/json
date: Mon, 22 Jan 2024 09:04:58 GMT
server: uvicorn

{
    "detail": [
        {
            "input": null,
            "loc": [
                "body",
                "who"
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.5/v/missing"
        }
    ]
}
```

Or using `requests` and Python's REPL, which requires you to pass the body as a dictionary in the `json` argument:


```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi", json={"who": "sergio"})
>>> r.status_code
200
>>> r.json()
'Hello? sergio?'
```
