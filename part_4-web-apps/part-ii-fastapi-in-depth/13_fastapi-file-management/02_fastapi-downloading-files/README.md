# FastAPI: uploading files using `File()` and `UploadFile`


## Setting up shop

This project is configured with Poetry.

```bash
$ poetry install
```

Then you can either do:

This project is configured with Poetry.

```bash
$ poetry run uvicorn hellofile.main:app --port 8080 --reload
```

or simply:

```bash
poetry run python hellofile/main.py
```

## Testing the endpoint with HTTPie

To test the file download in one shot you need to run the following command:

```bash
$ http localhost:8080/download-small-file/file1.txt
HTTP/1.1 200 OK
content-length: 104
content-type: text/plain; charset=utf-8
date: Thu, 07 Mar 2024 16:33:06 GMT
etag: "c1f898c4ea762a495565ca63ecea2581"
last-modified: Thu, 07 Mar 2024 16:31:35 GMT
server: uvicorn

This is line 1 of the sample file.
This is line 2 of the sample file.
This is line 3 of the sample file.
```

And for the image file:

```bash
$ http localhost:8080/download-small-file/beach.png | wc -c
740538
```

Same thing for the large files:

```bash
 http localhost:8080/download-large-file/file1.txt
HTTP/1.1 200 OK
Transfer-Encoding: chunked
date: Thu, 07 Mar 2024 17:02:34 GMT
server: uvicorn

This is line 1 of the sample file.
This is line 2 of the sample file.
This is line 3 of the sample file.

```

Note the chunked Transfer encoding.


```bash
$ http localhost:8080/download-large-file/beach.png
HTTP/1.1 200 OK
Transfer-Encoding: chunked
date: Thu, 07 Mar 2024 17:00:47 GMT
server: uvicorn



+-----------------------------------------+
| NOTE: binary data not shown in terminal |
+-----------------------------------------+
```


```bash
$ http localhost:8080/download-large-file/beach.png | wc -c
740538
```