# A simple GraphQL client based on Python using `requests`

## Description

This program is a simple GraphQL client written in Python that illustrates how to interact with the mock server you can start by following [00: Products Mock Server](../00-products-mock-server/).


### Setting up shop

The project uses venv for virtual environment management and pip for dependency management.

As a result, you just need to:

```bash
$ conda run -n web python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ pip install -r requirements.txt
```


To run the project, type:

```bash
flask run --reload
```

| NOTE: |
| :---- |
| You can customize the port using `flask run --port 5050`. |

The endpoints can be tested from the Swagger UI which you can find at http://localhost:5000/docs/kitchen (as configured in [`config.py`](config.py)).


Note that the Swagger endpoints are not created from the [manually created OpenAPI spec file](oas.yaml), but rather created automatically by Flask-smorest from the code.