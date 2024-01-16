# A "hello, world" GraphQL API server using Ariadne and uvicorn

## Description

This program is a simple GraphQL server based on the Ariadne framework.

The schema is defined inline in [server.py](./server.py) and a simple resolver that returns a random string for the `hello` operation is bound.


### Setting up shop

The project uses venv for virtual environment management and pip for dependency management.

As a result, you just need to:

```bash
$ conda run -n web python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ pip install -r requirements.txt
```


To run the project, type:

```bash
$ uvicorn server:server --port 8080 --reload
```

The GraphQL endpoint can be tested from the GraphiQL UI provided by Ariadne in `http://localhost:8080/`, or using curl:

```bash
$ curl --verbose 'http://localhost:8080/' \
  -H 'content-type: application/json'   \
  --data-raw '{"query":"{\n  hello\n}"}' \
  --compressed | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 127.0.0.1:8080...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8080 (#0)
> POST / HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.68.0
> Accept: */*
> Accept-Encoding: deflate, gzip, br
> content-type: application/json
> Content-Length: 25
>
} [25 bytes data]
* upload completely sent off: 25 out of 25 bytes
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< date: Tue, 09 Jan 2024 12:57:43 GMT
< server: uvicorn
< content-length: 31
< content-type: application/json
<
{ [31 bytes data]
100    56  100    31  100    25  15500  12500 --:--:-- --:--:-- --:--:-- 28000
* Connection #0 to host localhost left intact
{
  "data": {
    "hello": "ytinniYENn"
  }
}
```
