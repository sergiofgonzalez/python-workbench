# Cryptid service using FastAPI framework
> Step 5: taking a stab at logging

This project illustrates how to build a web application that implements the management of *cryptids* (imaginary creatures) and the explorers who seek them.

## Motivation

I haven't found any use of the `logging` module in the FastAPI examples I've reviewed so far (which is surprising!).

In this project I try to introduce a logging facility to make it easy for the webapp developers to log additional information in the console.

References:
+ https://www.sheshbabu.com/posts/fastapi-structured-json-logging/
+ https://github.com/sheshbabu/fastapi-structured-json-logging-demo

+ https://dev.to/tomas223/logging-tracing-in-python-fastapi-with-opencensus-a-azure-2jcm

+ https://github.com/alexperezortuno/playing-with-fastapi/blob/b6a63880087cba405b589bf125c24ede6d05af91/core/log_config.py

I start with a simple approach with the intention of making a logging config available to the developer so that logging configuration gets intertwined with FastAPI request logger.

## Using the `logger`

You can use the application logger in your code by simply doing:

```python
from cryptid.utils.log_config import get_logger


router = APIRouter(prefix="/explorer")


logger = get_logger(__name__)


@router.get("/")
def get_all() -> list[Explorer]:
    value = 5
    logger.info("What the heck? %s", value)
    return service.get_all()
```

By default, the logger will be customized to play well with the default uvicorn logging so that it outputs:

```
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     cryptid.web.explorer : application logging!!!
INFO:     127.0.0.1:43732 - "GET /explorer/ HTTP/1.1" 200 OK
```

The `get_logger()` function allows for a second argument if you want to customize the format:

```python
from cryptid.utils.log_config import get_logger
import logging


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger = get_logger(__name__, formatter=logging.Formatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%s"))

@router.get("/")
def get_all() -> list[Creature]:
    logger.info("Creatures everyhere!")
    return service.get_all()
```

which will output:

```
2024-02-08 14:16:1707398186 - cryptid.web.creature - INFO - Creatures everyhere!
INFO:     127.0.0.1:42130 - "GET /creature/ HTTP/1.1" 200 OK
```

The log level for the application logger can be configured with the `APP_LOG_LEVEL` environment variable. By default it is set to INFO.

```bash
$ APP_LOG_LEVEL=DEBUG python cryptid/main.py
INFO:     Application startup complete.
DEBUG:    cryptid.web.explorer : What the heck is that?
```

## Custom structured JSON logging

You can also do custom structured JSON logging using the approach implemented by `log_json.py`, `log_middleware.py` and how the middleware is imported into `main.py`.

This approach can be extended to include additional things comming in the log (not only for the access logging, but also for application logging).

## Customizing uvicorn logging

uvicorn log level can be customized through the CLI or the `run` method:

```bash
$ poetry run uvicorn cryptid.main:app \
  --log-level trace \
  --port 8080
INFO:     Started server process [171179]
INFO:     Waiting for application startup.
TRACE:    ASGI [1] Started scope={'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}}
TRACE:    ASGI [1] Receive {'type': 'lifespan.startup'}
TRACE:    ASGI [1] Send {'type': 'lifespan.startup.complete'}
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
TRACE:    127.0.0.1:33924 - HTTP connection made
TRACE:    127.0.0.1:33924 - ASGI [2] Started scope={'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.3'}, 'http_version': '1.1', 'server': ('127.0.0.1', 8080), 'client': ('127.0.0.1', 33924), 'scheme': 'http', 'method': 'GET', 'root_path': '', 'path': '/explorer/', 'raw_path': b'/explorer/', 'query_string': b'', 'headers': '<...>', 'state': {}}
TRACE:    127.0.0.1:33924 - ASGI [2] Send {'type': 'http.response.start', 'status': 200, 'headers': '<...>'}
INFO:     127.0.0.1:33924 - "GET /explorer/ HTTP/1.1" 200 OK
TRACE:    127.0.0.1:33924 - ASGI [2] Send {'type': 'http.response.body', 'body': '<153 bytes>'}
TRACE:    127.0.0.1:33924 - ASGI [2] Completed
TRACE:    127.0.0.1:33924 - HTTP connection lost
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
TRACE:    ASGI [1] Receive {'type': 'lifespan.shutdown'}
TRACE:    ASGI [1] Send {'type': 'lifespan.shutdown.complete'}
TRACE:    ASGI [1] Completed
```

The same result is obtained with the `run` method:

```python
uvicorn.run(
    "main:app",
    reload=True,
    port=int(os.getenv("PORT", "8080")),
    log_level="trace",
)
```

| NOTE: |
| :---- |
| The `log_level` setting only affects the uvicorn logger, not the application loggers. |


The uvicorn logging format can also be adjusterd using json/YAML or `dictConfig()` formats.

```python
    import uvicorn

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run(
        "main:app",
        reload=True,
        port=int(os.getenv("PORT", "8080")),
        log_config=log_config
    )
```

which makes the logging look like:

```
2024-02-08 14:52:58,224 - INFO - Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
2024-02-08 14:52:58,224 - INFO - Started reloader process [182110] using StatReload
2024-02-08 14:52:58,704 - INFO - Started server process [182118]
2024-02-08 14:52:58,705 - INFO - Waiting for application startup.
2024-02-08 14:52:58,705 - INFO - Application startup complete.
```


## Setting up shop

The project uses Poetry. To set things up type:

```bash
poetry install
```

## Running the application

To run the application in development mode type:

```bash
poetry run python cryptid/main.py
```

This will start the server in port 8080 with reloading enabled.

You can also run the application with `uvicorn`:

```bash
poetry run uvicorn cryptid.main:app \
  --port 8080 \
  --reload
```

## Testing the application

The implementation at this stage is a little bit all over the place as the web and data layer has not been adjusted.

There's a [unit test](tests/unit/service/test_creature.py) with the basic features.
