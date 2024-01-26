# Orders service using FastAPI
> Step 1: Early API Testing with Dredd and Dredd Hooks

## Description

This project illustrates how to use [Dredd](https://github.com/apiaryio/dredd) and [Dredd-hooks](https://github.com/apiaryio/dredd-hooks-python) to do early testing in your APIs.

The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml).


### Setting up shop

The project uses poetry.

As a result, you just need to type:

```bash
$ poetry install
```


To run the project, type:

```bash
poetry run uvicorn orders.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs. Alternatively, you can also go to http://localhost:8080/redoc which is an alternative visualization for REST APIs.

The project also includes HTTPie as a dev dependency for quick testing.

### Running the tests with Dredd

To run the tests using Dredd and the Dredd hooks implemented in [`./hooks`](hooks.py) type:

```bash
npx dredd oas.yaml http://localhost:8080 \
  --server "uvicorn orders.app:app --port 8080" \
  --hookfiles=./hooks.py --language=python
```

Note that you must run that command in an environment with the corresponding virtual environment activated.

The name of the tests can be obtained with the command:

```bash
npx dredd oas.yaml http://localhost:8080 \
  --names \
  --server "uvicorn orders.app:app --port 8080"
```

To run a specific test you can do:

```bash
npx dredd oas.yaml http://localhost:8080 \
  --only="/orders > Returns a list of orders > 200 > application/json" \
  --server "poetry run uvicorn orders.app:app --port 8080" \
  --hookfiles=./hooks.py --language=python
```