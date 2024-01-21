# A simple FastAPI app illustrating Pydantic integration

## Description

This is a simple FastAPI web app that exposes an endpoint `GET /creatures` that returns an array of `Creature` objects.

The model/schema is specified in `creatures/model.py` using Pydantic.


### Testing the application with HTTPie

#### Happy path

```bash
$ http localhost:8080/creatures --verbose
GET /creatures HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
content-length: 205
content-type: application/json
date: Sat, 20 Jan 2024 18:29:33 GMT
server: uvicorn

[
    {
        "aka": "Abominable Snowman",
        "area": "Himalayas",
        "country": "CN",
        "description": "Hirsute Himalayan",
        "name": "yeti"
    },
    {
        "aka": "Bigfoot",
        "area": "*",
        "country": "US",
        "description": "Yeti's cousin",
        "name": "sasquatch"
    }
]
```

### Testing that type Validation fails

A simple test has been added so that you can see typical error displayed when a type validation fails.

You can run it with:

```bash
python -m unittest discover -m
```