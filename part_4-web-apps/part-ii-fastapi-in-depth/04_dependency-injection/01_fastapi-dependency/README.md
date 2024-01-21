# FastAPI dependencies

## Description

This application illustrates how you can create your own custom dependency which will be called and provided to your path function by FastAPI automatically.

The following use cases are illustrated in the example

1. `GET /user` &mdash; a `user_dep` function is defined which is supposed to extract from the query parameters `name` and `password` some data which is then injected into the path function.

2. `GET /v2/user` &mdash; illustrates an alternative syntax for the same functionality as the previous point.

3. `GET /checkuser` &mdash; a dependency that just checks something and doesn't return anything. The depedency is stated in the decorator itself.

### Testing with HTTPie

For point #1:

```bash
$ http localhost:8080/user name==sergio password==secret
HTTP/1.1 200 OK
content-length: 30
content-type: application/json
date: Sat, 20 Jan 2024 19:46:36 GMT
server: uvicorn

{
    "name": "sergio",
    "valid": true
}

```

For point #2:

```bash
$ http localhost:8080/v2/user name==sergio password==secret
HTTP/1.1 200 OK
content-length: 30
content-type: application/json
date: Sun, 21 Jan 2024 08:26:36 GMT
server: uvicorn

{
    "name": "sergio",
    "valid": true
}
```

For point #3:

Happy path:

```bash
$ http localhost:8080/user/check name==jason
HTTP/1.1 200 OK
content-length: 4
content-type: application/json
date: Sun, 21 Jan 2024 08:36:25 GMT
server: uvicorn

true

```

Unhappy path

```bash
$ http localhost:8080/user/check name==sergio password==secret
HTTP/1.1 500 Internal Server Error
content-length: 21
content-type: text/plain; charset=utf-8
date: Sun, 21 Jan 2024 08:34:44 GMT
server: uvicorn

Internal Server Error
```

$ http localhost:8080/user/check name==sergio password==secret
HTTP/1.1 500 Internal Server Error
content-length: 21
content-type: text/plain; charset=utf-8
date: Sun, 21 Jan 2024 08:34:44 GMT
server: uvicorn

Internal Server Error

