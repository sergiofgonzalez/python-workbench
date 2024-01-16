# Implementing a Kitchen service using flask-smorest
> Step 1: Adding validation

## Description

This project adds request, URL query parameter, and response payload validation for for the Kitchen Service example [04: Kitchen Service using Flask-smorest](../04-flask-smorest-kitchen-svc/). The API implemented is described by the [Kitchen OpenAPI spec](./oas.yaml).


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