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