# Hello, FastAPI with In-Memory Order Management
> basic FastAPI + validations + basic order management

## Description

This project is an enhancement of [Hello, FastAPI](../02-hello-fastapi/README.md) in which a very basic in-memory order management is implemented to be able to respond non-hardcoded responses.

### Setting up shop

The project uses Pipenv for dependency management. The `pipfile` and `pipfile.lock` come from the other project.

In order to start up things you need to:

1. Activate the conda web virtual environment

    ```bash
    $ conda deactivate
    $ conda activate base
    ```

2. Run `pipenv shell` to activate the pipenv managed virtual environment which is created under `~.local/share/virtualenvs`.

    ```bash
    $ pipenv shell
    ```

3. Run `pipenv install` which will read the `pipfile` and `pipfile.lock` and install the requirements from there.

    ```bash
    $ pipenv install
    ```

4. Run the web project:

    ```bash
    uvicorn orders.app:app --reload --port 8080
    ```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs. Alternatively, you can also go to http://localhost:8080/redoc which is an alternative visualization for REST APIs.

Those descriptions are not created from the [manually created OpenAPI spec file](oas.yaml), but rather created automatically by FastAPI from our code.