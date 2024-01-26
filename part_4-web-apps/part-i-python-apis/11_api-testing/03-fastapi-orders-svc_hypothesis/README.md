# Orders service using FastAPI
> Step 3: Property-based API Testing with PyTest and Hypothesis

## Description

This project illustrates how to use Hypothesis to do property-based testing on the APIs.

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

### Running the property-based tests with PyTest

To run the tests you can either run them within Visual Studio Code, or in the terminal running:

```bash
poetry run pytest
```

You should get a result with a few warnings but the final line should indicate that both tests ended up successfully:

```
=========================== 1 passed, 3 warnings in 3.01s ===========================
```