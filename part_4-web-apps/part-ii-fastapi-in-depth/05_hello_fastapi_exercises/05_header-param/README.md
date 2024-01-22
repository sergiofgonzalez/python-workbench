# Exercise 05: Header parameter management
> illustrates how to manage endpoints that expect information in http headers of the request using FastAPI

## Description

This application exposes an endpoint `GET /hi` that expects a query parameter `who` including the name to greet to be able to return the following JSON string `"Hello? {who}?"`.


### Starting the project

You can start the project with:

```bash
uvicorn fastapi-svc.web:app --port 8080 --reload
```

### Testing the projects

You can test the GET endpoint with HTTPie:

```bash
$ http localhost:8080/hi who:sergio --verbose
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2
who: sergio



HTTP/1.1 200 OK
content-length: 16
content-type: application/json
date: Mon, 22 Jan 2024 09:17:59 GMT
server: uvicorn

"Hello? sergio?"
```

The `GET /hi` endpoint without sending the parameter should return a `"422 Unprocessable Entity"`:

| NOTE: |
| :---- |
| A `422 (Unprocessable Entity)` should be sent when sending a malformed payload that is syntactically correct, but missing a required parameters, or containing an invalid parameter, or assigning a wrong value or type to a parameter. |


```bash
$ http localhost:8080/hi --verbose
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 422 Unprocessable Entity
content-length: 140
content-type: application/json
date: Mon, 22 Jan 2024 09:18:38 GMT
server: uvicorn

{
    "detail": [
        {
            "input": null,
            "loc": [
                "header",
                "who"
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.5/v/missing"
        }
    ]
}
```

Or using `requests` and Python's REPL, which requires you to pass the header values in the `headers` argument:


```python
>>> import requests
>>> r = requests.get("http://localhost:8080/hi", headers={"who": "sergio"})
>>> r.status_code
200
>>> r.json()
'Hello? sergio?'
```
