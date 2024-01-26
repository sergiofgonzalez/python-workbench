# Orders service using FastAPI
> Step 3 (unittest variant): Property-based API Testing with PyTest and Hypothesis

## Description

This project illustrates how to use Hypothesis to do property-based testing on the APIs. The tests are implemented with unittest instead of PyTest (where it seems to be easier to get more information on the payloads Hypothesis is generating).

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

### Running the property-based tests with unittest

To run the tests you can either run them within Visual Studio Code, or in the terminal running:

```bash
$ python -m unittest discover
```

You should get the results with the Hypothesis verbosity:

```
Trying example: test_orders(
    self=<tests.test_orders.TestOrderCreation testMethod=test_orders>,
    payload={'product': False,
     'size': 'medium',
     'quantity': '\x81\U0001a705\x89'},
)
Trying example: test_orders(
    self=<tests.test_orders.TestOrderCreation testMethod=test_orders>,
    payload={'product': False,
     'size': 'medium',
     'quantity': '\x81\U0001a705\x89'},
)
ok

----------------------------------------------------------------------
Ran 1 test in 3.377s

OK
```