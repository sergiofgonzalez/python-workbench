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


