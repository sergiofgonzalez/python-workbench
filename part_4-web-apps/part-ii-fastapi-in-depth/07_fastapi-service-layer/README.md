# FastAPI in depth: Building the Web Layer

## Service Layer

At the RESTful router, the resources are the nouns: creatures and explorers.

The service layer sits in the middle of the web that exposes the API and the data.

It's common to initially implement the service layer as a pass-through between the web and the data layer. It's also common to use the service layer to codify the required the application business logic as new requirements are introduced in the application.

## Logging

FastAPI automatically logs each API call to an endpoint:

```
INFO:     127.0.0.1:56400 - "GET /explorer/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:38442 - "GET /explorer/Noah%20Weise HTTP/1.1" 200 OK
INFO:     127.0.0.1:56400 - "PUT /explorer/Noah%20Weise HTTP/1.1" 405 Method Not Allowed
INFO:     127.0.0.1:56638 - "PUT /explorer/ HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:50822 - "GET /creature/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:33838 - "GET /creature/Bigfoot HTTP/1.1" 200 OK
```

However, FastAPI will not automatically log any data delivered via the body or headers.

## Metrics, Monitoring, Observability

If you run a website, you might want to know which endpoints are being accessed, how many people are visiting the page, etc. These type of statistics are called *metric*, and the gathering of them is called *monitoring* or *observability*.

The de-facto standards these days for such concerns are [Prometheus](https://prometheus.io/) for gathering metrics and [Grafana](https://grafana.com/) for displaying them.

## Tracing

It's common for metrics to be good overall, but with certain concerns in some specific area.

It's useful to have a tool that measures how an an API call takes, end-to-end, reporting the time taken in each individual step, so that you can pinpoint where your problems are found. This is called *tracing*.

The open source project [OpenTelemetry](https://opentelemetry.io/), which is managed under the CNCF umbrella, has taken over earlier tracing products such as Jaeger. OpenTelemetry features a [Python API](https://opentelemetry.io/docs/languages/python/) and can be integrated with FastAPI.

