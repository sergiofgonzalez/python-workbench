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