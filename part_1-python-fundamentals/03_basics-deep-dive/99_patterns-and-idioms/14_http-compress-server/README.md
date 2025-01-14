# Time efficiency using streams in a complex example

Let's consider a more complex example, involving an application with two subcomponents.

The client side of the application will compress a file, and send it to a remote HTTP server. In turn, the server side of the application will be listening to incoming requests that will assume to be gzipped files that will decompress and save them in the file system.

This is a good scenario for streams, as we wouldn't want the client to materialize the file before being able to send it to the server, and we wouldn't want to the server to recreate the file in memory before it can save it (imagine the server handling multiple concurrent requests involving large files!).

Therefore:
+ on the client side we will use streams to allow compressing the information and sending data chunks as soon as they're read from the file system.
+ on the server side, we will use streams to decompress every chunk as soon as it is received, writing each chunk as we receive it.

## Testing the server


The server is started normally:

```python
uv run server.py
```

By default the server is registered on port 8000. You can use the option `--port` to use run the server in other port.

```python
uv run server.py --port 5000
```

In order to test the server in isolation, you can use [httpie](https://httpie.io/):

```bash
# send the README.md file
$ http PUT localhost:5000/hello "x-filename: README.md" "Content-Type: application/octet-stream" < README.md
```

Note that [httpie](https://httpie.io/) will also send the required `Content-Length` HTTP header behind the scenes, as it is required by the server (otherwise, the `request.rfile.read()` operation will block forever).

### server_v0

The first version that accepts files, but does not assume that the file comes gzipped.

### server_v1

This version accepts gzipped files. Can work with `client_v3.py`

### server_v2

See [Rationale for change of direction](#change-of-direction-rationale).

## Testing the client

### client_v0

A basic test checking how we can produce a gzip stream.

### client_v1

First try using the approach from v0, which doesn't work because it assumes a chunked Transfer-Encoding:

```python
for k, v in request.headers.items():
    print(f"{k}: {v}")
Host: localhost:8000
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Type: application/octet-stream
X-Filename: README.md
Content-Encoding: gzip
Transfer-Encoding: chunked
```

### client_v2

Leaving out the gzip requirement, that is, sends the file as is. It works with `server_v0.py`.

### client_v3

Sends the file compressed, although I'm not sure it is actually streamed.



## Change of direction: Rationale

At this point I've realized that in server_v1 I'm reading more bytes than the gzipped chunk, so it's better to change the approach and use chunking instead. Otherwise, I'd need to send separately the length of each compressed chunk.

Therefore, next exercise is to understand how `httpie` works with chunks and then try to accomplish on the server and then on the client.

### server_v2

Implementation that handles **chunking** without gzipping using httpie client.

When sending a request such as:

```bashblock
http --chunked PUT localhost:8000 "x-filename: SOME_FILE.md" @SOME_FILE.md
```

We get the following HTTP headers:

```
'Host': 'localhost:8000'
'Accept-Encoding': 'gzip, deflate'
'Connection': 'keep-alive'
'Transfer-Encoding': 'chunked'
'User-Agent': 'HTTPie/3.2.3'
'Accept': 'application/json, */*;q=0.5'
'Content-Type': 'text/markdown'
'x-filename': 'SOME_FILE.md'
```

Note that in the first request, there's no "Content-Length". However, this can be solved by understanding a bit more the protocol involved in a chunked request:

For every line in a chunked request the client sends we find:
+ A line that includes the chunk length (so that we will be able to read the chunk with `file.read()`).
+ Then contents of the chunk.
+ An extra "\r\n".

You can test this server with the command:

```bash
http --chunked PUT localhost:8000 "x-filename: SOME_FILE.md" @SOME_FILE.md
```

### server_v3

Implementation that handles gzipping using httpie client.

You can test it with:

```bash
# send the README.md file
$ http -xx PUT localhost:8000 "x-filename: SOME_FILE.md" @SOME_FILE.md
```

Note that you need to use `zlib` as httpie uses `deflate` as the `Content-Encoding`.