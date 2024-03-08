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

To test the file upload you need to run the following command:

```bash
$ http --form POST localhost:8080/upload-small-file \
  uploaded_file@"/home/ubuntu/.bashrc"
HTTP/1.1 200 OK
content-length: 27
content-type: application/json
date: Thu, 07 Mar 2024 11:25:15 GMT
server: uvicorn

"File size: 60058024 bytes"
```

Note that you need to include `--form` (or `-f`) before `POST`, and that the `uploaded_file` portion indicates what is the name of the variable in the corresponding path function.


For the `UploadFile` method:

```bash
$ http --form POST localhost:8080/upload-large-file uploaded_file@"/home/ubuntu/large_file.bin"
HTTP/1.1 200 OK
content-length: 28
content-type: application/json
date: Thu, 07 Mar 2024 14:44:09 GMT
server: uvicorn

"File size: 256389948 bytes"
```

## Testing the endpoint with `requests`

It's really easy to test the endpoint programmatically with the `requests` module too:

```python
>>> import requests
>>> url = "http://localhost:8080/upload-small-file"
>>> files = {"uploaded_file": open("/home/ubuntu/.bashrc", "rb")}
>>> response = requests.post(url, files=files)
>>> response.json()
'File size: 7581 bytes'
>>> response.status_code
200
```