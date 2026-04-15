# {{cookiecutter.project_index}}: {{cookiecutter.project_readme_title}}
> {{cookiecutter.project_description}}

## Project description

ToDo

### TODO: illustrate what to do to develop some intuition on the concepts

ToDo

## Running the program

You can run the application with:

```bash
uv run fastapi dev --port {port}
```

## Running your tests

You can run the tests from your IDE or from the command line using:

```bash
uv run pytest
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

PyTest (+ `pytest-sugar` + `pytest-cov`) and Ruff were also added as dev dependencies:

```bash
$ uv add pytest pytest-sugar pytest-cov --dev
```
