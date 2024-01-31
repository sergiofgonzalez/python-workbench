# Dockerizing microservice APIs

+ How to dockerize an application
+ How to use Docker Compose to run an application
+ Publishing a Docker image to AWS ECR

## Intro

In this chapter, we will see how to Dockerize a Python application. We will focus on dockerizing (i.e., making an application run as a Docker container) the Orders service.

## Dockerizing the Orders Service

In our first take, we take a simplistic approach that pretty much resembles how we run the application in our local environment:

```dockerfile
FROM python:3.10-slim

LABEL maintainer="sergio.f.gonzalez@gmail.com"
ENV REFRESHED_AT "2024-01-29 09:23:14.443427"

# Use SQLite as the default DB engine
ENV DB_URL=sqlite:///orders.db

RUN mkdir -p /orders_svc/orders

WORKDIR /orders_svc

COPY pyproject.toml poetry.lock /orders_svc/

# Create virtual environment within the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install -U poetry && poetry install --no-root --no-directory --without dev


COPY orders/orders_service /orders_svc/orders/orders_service
COPY orders/repository /orders_svc/orders/repository
COPY orders/web /orders_svc/orders/web
COPY oas.yaml /orders_svc/oas.yaml
COPY public_key /orders_svc/public_key

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "orders.web.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

The only relevant details of this first version are:

+ We use `python:3.10-slim` as the base image
+ We define the default value for `DB_URL` and configure it to point to a local file named `orders.db` (as we do when running without a container).
+ We create a directory `orders_svc/` within the container to host our application artifacts.
+ We copy the `pyproject.toml` and the corresponding lockfile, install poetry and install without the dev dependencies. Note that we instruct poetry to install the virtual environment within the project.
+ We copy the corresponding relevant sources to `orders_svc/`
+ We define 8080 as the default port for the web app
+ We run the application with `poetry run`

## Improving the container image with multi-stage builds

The previous image can be made more flexible and at the same time improve its size by using build arguments and multi-stage builds.

By adding build args, you can use the same Dockerfile template for different microservices (no matter the name):

```dockerfile
# Global build args
ARG APP_BASE_PATH=/home/pyuser/app
ARG APP_PACKAGE_NAME=web_svc

# Stage 1: Install dependencies
FROM python:3.10-slim as builder

ARG APP_BASE_PATH

WORKDIR $APP_BASE_PATH

COPY pyproject.toml poetry.lock ./

# Create virtual environment within the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install -U poetry
RUN poetry install --no-root --no-directory --without dev

# Stage 2: Prepare runtime
FROM python:3.10-slim as runtime

ARG APP_BASE_PATH
ARG APP_PACKAGE_NAME


WORKDIR $APP_BASE_PATH

COPY orders/ ./$APP_PACKAGE_NAME
COPY oas.yaml ./
COPY public_key ./

COPY --from=builder $APP_BASE_PATH/.venv/ ./.venv

ENV PATH=$APP_BASE_PATH/.venv/bin:$PATH
ENV DB_URL=sqlite:///orders.db

EXPOSE 8080

ENV PY_APP_PACK_NAME=$APP_PACKAGE_NAME

CMD exec uvicorn ${PY_APP_PACK_NAME}.web.app:app --host 0.0.0.0 --port 8080
```

The relevant parts are:

a couple of build arguments are defined:
  + `APP_BASE_PATH` &mdash; path to where the application will be installed in the container's file system. The default value is set to `/home/pyuser/app`.
  + `APP_PACKAGE_NAME` &mdash; the name of the app package (i.e., `orders` for this microservice). The default value is set to `web_svc`.

In the first stage of the build, we just install Poetry and the dev dependencies.

In the second stage, we prepare the runtime by copying only the virtual environment and the sources needed.

Because we want to make the `Dockerfile` generic, we want to use a variable in the command. This requires a special approach. First of all, build arguments cannot be used in `CMD` (`CMD` is a runtime thing, while build arg applies only to build time). This can be worked around using environment variables.

The default way of encoding a command is through a JSON array as in:

```dockerfile
CMD ["command", "param1", "param2"]
```

However, when doing so, you cannot use environment variables.

You can use instead something like:

```dockerfile
CMD "command $var param2"
```

but this results in the command being passed to the shell, so the process will show:

```bash
/bin/sh -c uvicorn orders.web.app:app --host 0.0.0.0 --port 8080
```

This might have unintended consequences when trapping signals. In order to solve it, you need to use:

```dockerfile
CMD exec uvicorn ${PY_APP_PACK_NAME}.web.app:app --host 0.0.0.0 --port 8080
```

When using `exec` you end up running the app directly, and not passed through the shell:

```dockerfile
/home/pyuser/app/.venv/bin/python /home/pyuser/app/.venv/bin/uvicorn orders.web.app:app
```

| NOTE: |
| :---- |
| If you find that `ps` is not available in your Docker image you can install it using `apt update && apt install procps`. |

## Securing the container with a non-root user

In the final installment of our container, we introduce a few changes leading to a container that is not running as user named `monty` instead of root.

```dockerfile
# Global build args
ARG APP_BASE_PATH=/home/monty/app

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Stage 1: Install dependencies on a virtual env managed by Poetry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM python:3.10-slim as builder

# Reference global build arg so that it can be used in this stage
ARG APP_BASE_PATH

# Set working directory for subsequent COPY and RUN operations
WORKDIR $APP_BASE_PATH

# Copy pyproject.toml and lockfile to the app's base directory
COPY pyproject.toml poetry.lock ./

# Install Poetry in a separate virtual environment (as recommended)
ENV POETRY_HOME=/opt/poetry
RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install poetry

# Install project's runtime dependencies in app's base directory
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN ${POETRY_HOME}/bin/poetry install --no-root --no-directory --without dev

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Stage 2: Prepare runtime
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM python:3.10-slim as runtime

# Reference global build arg so that it can be used in this stage
ARG APP_BASE_PATH

# Define app's package name as a build-arg
ARG APP_PACKAGE_NAME=web_svc

# Create user `monty` and switch to it
ARG GID=1000
ARG UID=1000
RUN groupadd -g "${GID}" monty
RUN useradd --create-home --no-log-init -u "${UID}" -g "${GID}" monty
USER monty

# Set working directory for COPY and CMD operations
WORKDIR $APP_BASE_PATH

# Copy application resources to the corresponding directories
COPY --chown=monty:monty orders/ ./$APP_PACKAGE_NAME
COPY --chown=monty:monty oas.yaml ./
COPY --chown=monty:monty public_key ./

# Copy the virtualenv from previous stage
COPY --chown=monty:monty --from=builder $APP_BASE_PATH/.venv/ ./.venv

# Make virtual env binaries available in the $PATH
ENV PATH=$APP_BASE_PATH/.venv/bin:$PATH

# Set the default DB_URL to point to a file `orders.db` in the current dir
ENV DB_URL=sqlite:///orders.db

# Inform Docker that the container will listen in 8080 at runtime
EXPOSE 8080

# Map a build arg into an env var so that CMD is configurable and start server
ENV PY_APP_PACK_NAME=$APP_PACKAGE_NAME
CMD exec uvicorn ${PY_APP_PACK_NAME}.web.app:app --host 0.0.0.0 --port 8080
```

The first stage contains only minor changes to align poetry recommendations. Note that in this first stage, we use the root user for the installation and configuration as that simplifies things with pip and poetry. We also install poetry in its own virtualenv, so that it doesn't get mixed with the rest of the dependencies in the container or the project.

In the second stage is where we introduced the non-root user `monty`. As the Python user does not come with a non-root user, we define it, and assign to it the ID=100 and GID=1000, as some documentation suggests that not doing so can lead to problems in the management of volumes.

Immediately after having created the user we switch to it, making the rest of operations under that user permissions, which limits the surface attack of the container (e.g., that user cannot run `apt install`).

Then we copy only the relevant artifacts from the `builder` stage with the approrpiate permissions, and make the virtual environment that we've copied available in the PATH for the user.

Finally, we execute `uvicorn` to start the server.

