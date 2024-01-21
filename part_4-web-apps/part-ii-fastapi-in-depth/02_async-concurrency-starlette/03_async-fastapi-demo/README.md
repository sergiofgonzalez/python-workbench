# Async FastAPI demo
> a very simple FastAPI application using async/await

## Running the application

You can run the application doing:

```python
uvicorn hello.server:app --port 8080 --reload
```

## Testing the application with HTTPie

You can type:

```bash
$ http localhost:8080/hi
HTTP/1.1 200 OK
content-length: 23
content-type: application/json
date: Sat, 20 Jan 2024 09:23:37 GMT
server: uvicorn

"Hello, async FastAPI!"

```