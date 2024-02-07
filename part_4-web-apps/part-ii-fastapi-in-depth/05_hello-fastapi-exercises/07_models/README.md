# Exercise 07: FastAPI Model/Schema Managemenent and Validations
> illustrates how to do basic model/schema management and request/response payload validation in FastAPI

## Description

This application implements a very basic task management application that lets you create tasks defined with the following fields:

+ title &mdash; string, required
+ description &mdash; string, optional
+ urgency &mdash; integer

Once created, tasks are given an internal UUID and a `creation_ts` field.

The application also lets you retrieve the list of created tasks.


### Starting the project

You can start the project with:

```bash
uvicorn fastapi-svc.web:app --port 8080 --reload
```

### Testing the projects

Things to test:
- [X] 1: Retrieving all when empty returns empty list
- [X] 2: Creating one task return task with `creation_ts` field
- [X] 3: Retrieving all after having created one task returns that task with `creation_ts` extra field, no id
- [X] 4: Retrieving all after having created two tasks return those tasks with extra field, no ids
- [X] 5: Sending empty or incomplete task fails
- [X] 6: Creating a task without description works OK
- [ ] 7: Creating a task with title length below min or description below min, or urgency out of range fails.

You can test the app with HTTPie:

#### 6: Creating a task without description works OK

Creating a task with title length below min or description below min, or urgency out of range fails.

```bash
$ http post localhost:8080/tasks title="X" urgency=
5 -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 30
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "title": "X",
    "urgency": "5"
}


HTTP/1.1 422 Unprocessable Entity
content-length: 206
content-type: application/json
date: Mon, 22 Jan 2024 13:03:11 GMT
server: uvicorn

{
    "detail": [
        {
            "ctx": {
                "min_length": 2
            },
            "input": "X",
            "loc": [
                "body",
                "title"
            ],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.5/v/string_too_short"
        }
    ]
}
```

```bash
$ http post localhost:8080/tasks title="Finish reading FastAPI book" description="G" urgency=3 -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 76
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "description": "G",
    "title": "Finish reading FastAPI book",
    "urgency": "3"
}


HTTP/1.1 422 Unprocessable Entity
content-length: 212
content-type: application/json
date: Mon, 22 Jan 2024 13:03:56 GMT
server: uvicorn

{
    "detail": [
        {
            "ctx": {
                "min_length": 2
            },
            "input": "G",
            "loc": [
                "body",
                "description"
            ],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.5/v/string_too_short"
        }
    ]
}
```

```bash
$ http post localhost:8080/tasks title="Finish reading FastAPI book" description="Gffss" urgency=0 -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 80
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "description": "Gffss",
    "title": "Finish reading FastAPI book",
    "urgency": "0"
}


HTTP/1.1 422 Unprocessable Entity
content-length: 206
content-type: application/json
date: Mon, 22 Jan 2024 13:04:35 GMT
server: uvicorn

{
    "detail": [
        {
            "ctx": {
                "ge": 1
            },
            "input": "0",
            "loc": [
                "body",
                "urgency"
            ],
            "msg": "Input should be greater than or equal to 1",
            "type": "greater_than_equal",
            "url": "https://errors.pydantic.dev/2.5/v/greater_than_equal"
        }
    ]
}
```

```bash
$ http post localhost:8080/tasks title="Finish reading FastAPI book" description="Gffss" urgency=10 -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 81
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "description": "Gffss",
    "title": "Finish reading FastAPI book",
    "urgency": "10"
}


HTTP/1.1 422 Unprocessable Entity
content-length: 198
content-type: application/json
date: Mon, 22 Jan 2024 13:04:57 GMT
server: uvicorn

{
    "detail": [
        {
            "ctx": {
                "le": 9
            },
            "input": "10",
            "loc": [
                "body",
                "urgency"
            ],
            "msg": "Input should be less than or equal to 9",
            "type": "less_than_equal",
            "url": "https://errors.pydantic.dev/2.5/v/less_than_equal"
        }
    ]
}
```

#### 6: Creating a task without description works OK

```bash
$ http post localhost:8080/tasks title="Splunk" urg
ency=2 -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 35
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "title": "Splunk",
    "urgency": "2"
}


HTTP/1.1 200 OK
content-length: 92
content-type: application/json
date: Mon, 22 Jan 2024 13:01:19 GMT
server: uvicorn

{
    "creation_ts": "2024-01-22T13:01:20.677979",
    "description": null,
    "title": "Splunk",
    "urgency": 2
}
```


#### 5: Sending empty or incomplete task fails

Empty request

```bash
$ http post localhost:8080/tasks -v
POST /tasks HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 422 Unprocessable Entity
content-length: 132
content-type: application/json
date: Mon, 22 Jan 2024 12:56:59 GMT
server: uvicorn

{
    "detail": [
        {
            "input": null,
            "loc": [
                "body"
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.5/v/missing"
        }
    ]
}
```

Incomplete request:

```bash
$ http post localhost:8080/tasks title="Finish reading FastAPI book" description="Go through the authentication chapter" -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 96
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "description": "Go through the authentication chapter",
    "title": "Finish reading FastAPI book"
}


HTTP/1.1 422 Unprocessable Entity
content-length: 231
content-type: application/json
date: Mon, 22 Jan 2024 12:57:58 GMT
server: uvicorn

{
    "detail": [
        {
            "input": {
                "description": "Go through the authentication chapter",
                "title": "Finish reading FastAPI book"
            },
            "loc": [
                "body",
                "urgency"
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.5/v/missing"
        }
    ]
}
```



#### 4: Retrieving all after having created two tasks return those tasks with extra field, no ids

```bash
$ http localhost:8080/tasks -v
GET /tasks HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 282
content-type: application/json
date: Mon, 22 Jan 2024 12:55:32 GMT
server: uvicorn

[
    {
        "creation_ts": "2024-01-22T12:49:30.594956",
        "description": "stop coding and have the packed lunch",
        "title": "Have lunch",
        "urgency": 1
    },
    {
        "creation_ts": "2024-01-22T12:55:25.582968",
        "description": "Go through the authentication chapter",
        "title": "Finish reading FastAPI book",
        "urgency": 3
    }
]
```


#### 3: Retrieving all after creating one task returns that task with `creation_ts` extra field, no id

```bash
$ http localhost:8080/tasks -v
GET /tasks HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 133
content-type: application/json
date: Mon, 22 Jan 2024 12:52:37 GMT
server: uvicorn

[
    {
        "creation_ts": "2024-01-22T12:49:30.594956",
        "description": "stop coding and have the packed lunch",
        "title": "Have lunch",
        "urgency": 1
    }
]
```




#### 2: Creating one task return task with extra field

```bash
$ http post localhost:8080/tasks title="Have lunch" description="stop coding and have the packed lunch" urgency=1 -v
POST /tasks HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 95
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "description": "stop coding and have the packed lunch",
    "title": "Have lunch",
    "urgency": "1"
}


HTTP/1.1 200 OK
content-length: 131
content-type: application/json
date: Mon, 22 Jan 2024 12:49:30 GMT
server: uvicorn

{
    "creation_ts": "2024-01-22T12:49:30.594956",
    "description": "stop coding and have the packed lunch",
    "title": "Have lunch",
    "urgency": 1
}

```



#### 1: Retrieving all when empty returns empty list

```bash
$ http localhost:8080/tasks -v
GET /tasks HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 2
content-type: application/json
date: Mon, 22 Jan 2024 12:00:48 GMT
server: uvicorn

[]
```

