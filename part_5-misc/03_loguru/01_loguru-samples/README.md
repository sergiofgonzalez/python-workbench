# Loguru samples

## Setting up shop

Project was created with `uv`:

```bash
uv init 01_loguru-samples
```

Ruff is used for linting. The `pyproject.toml` has been initially configured with:

```toml
[tool.ruff]
# Set the maximum line length to 80
line-length = 80

[tool.ruff.lint]
ignore = [
    "T201",   # Allow print statements
    "ERA001", # Allow commented-out code
    "D212",   # Allow flexible style for multiline docstring
    "S311",   # Don't care about cryptographic safety
]

select = ["ALL"]
```

Loguru was also added using:

```bash
uv add loguru
```