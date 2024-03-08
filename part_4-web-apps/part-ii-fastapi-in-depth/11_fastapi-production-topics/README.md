# FastAPI: Production topics

## Deployment

The following sections give a brief overview about certain deployment considerations when working with FastAPI servers.

### Multiple workers

[Gunicorn](https://gunicorn.org/) is as WSGI (instead of ASGI) server, but it is possible to use it as a supervisor if you need to support hundreds or thousands of requests per second.

The documentation about how to do that can be found in [FastAPI: Server Workers - Gunicorn with Uvicorn](https://fastapi.tiangolo.com/deployment/server-workers/).

In essence, you'll need to do something like:

```bash
gunicorn main:appp --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8080
```

Uvicorn itself also can be used with multiple workers:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

but this method doesn't act as a process supervisor, so the gunicorn way described earlier is considered more robust.


### HTTPS

FastAPI documentation describes in its [FastAPI: About HTTPS](https://fastapi.tiangolo.com/deployment/https/) how to add HTTPS support to FastAPI by using [Traefik](https://github.com/traefik/traefik) and [Let's Encrypt](https://letsencrypt.org/).

### Docker

Again, the documentation from FastAPI gives a great overview about how to containerize your FastAPI application and a few recommendations when hosting your application behind a reverse proxy. See [FastAPI: Docker](https://fastapi.tiangolo.com/deployment/docker/).

### Cloud Services

FastAPI applications can be deployed on Cloud services such as AWS Lambda. You only need wrap the API with a handler such as [Mangum](https://github.com/jordaneremieff/mangum)

### Kubernetes

The blog post https://sumanta9090.medium.com/deploying-a-fastapi-application-on-kubernetes-a-step-by-step-guide-for-production-d74faac4ca36 illustrates how to deploy a FastAPI application on minikube.


## Performance

While Python is a relatively slow language, the use of ASGI and non-blocking I/O allows your FastAPI application to be extremely fast.

### Async

Any code in your web app has to wait for a response is a good candidate for using an `async` function. This will instruct FastAPI to do other things until the response is ready.

### Caches

If you have a web endpoint that gets some data from a static source it'll be typically much fast to *cache* it. Python provides the `cache()` and `lru_cache()` functions in the `functools` module to do so in your application.


### Queues

For tasks taking longer than a fraction of a second, it is recommended to handle it with a job queue like [Celery](https://docs.celeryq.dev/en/stable/).


### Metrics

The common practice in Python is to use:
+ [Prometheus](https://prometheus.io/) to gather metrics.
+ [Grafana](https://grafana.com/) to display them.
+ [OpenTelemetry](https://opentelemetry.io/) to measure timing and tracing capabilities.


## Review