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
