# Using FastAPI `response_model` to illustrate automatic file filtering

## Description

This simple application illustrates how you can use the `response_model` of the path decorator to filter out parts of the response you don't want to make available in the response.


To start the application run:

```bash
uvicorn tags.server:app --port 8080 --reload
```

### Testing the functionality with HTTPie

To create a tag you just need to provide a body like:

```json
{
  "tag": "<tagname>"
}
```

Thus,

```bash
$ http post localhost:8080/ tag=awesome
HTTP/1.1 201 Created
content-length: 17
content-type: application/json
date: Fri, 19 Jan 2024 13:17:45 GMT
server: uvicorn

{
    "tag": "awesome"
}
```


You can retrieve it using:

```bash
$ http localhost:8080/awesome
HTTP/1.1 200 OK
content-length: 56
content-type: application/json
date: Fri, 19 Jan 2024 13:17:50 GMT
server: uvicorn

{
    "created": "2024-01-19T13:17:45.980876",
    "tag": "awesome"
}
```