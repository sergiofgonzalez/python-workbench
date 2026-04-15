# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run dev server (default port 8000, or specify with --port)
uv run fastapi dev --port 5000

# Run all tests (with coverage + verbose output, configured in pyproject.toml)
uv run pytest

# Run a single test file
uv run pytest tests/unit/test_greeter.py

# Run a single test
uv run pytest tests/unit/test_greeter.py::test_read_greetings

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

## Architecture

This is a FastAPI orders microservice using an in-memory dict as the data store (intended to be replaced with SQLAlchemy + SQLite).

- `app/main.py` - Creates the FastAPI app and registers routers. The package is named `app` so `fastapi dev` autodiscovers it.
- `app/api/orders.py` - All order CRUD endpoints as an `APIRouter` mounted at `/orders`. State lives in `fake_orders_db` (a module-level dict).
- `app/api/schemas.py` - Pydantic models for request validation (`CreateOrderSchema`), response serialization (`GetOrderSchema`, `GetOrdersSchema`), and query params (`ReadOrdersQueryParams`). All schemas use `extra = "forbid"`.
- `tests/unit/` - Tests use `fastapi.testclient.TestClient` against the app directly (no server needed).

All functions use type annotations for parameters and return types.

For HTTP status codes, use `fastapi.status` constants (e.g., `status.HTTP_201_CREATED`) rather than raw integer values.

## Linting

Ruff is configured with **all rules enabled** (`select = ["ALL"]`). Notable exceptions:
- `T201` is ignored globally (print statements allowed)
- `S101` and `PLR2004` are ignored in `tests/` (assert and magic values allowed)
- Docstring convention: Google style
