# Grokking entity relationships
> understanding entity relationships with SQLAlchemy Core and ORM

## Setting up shop

```bash
uv init 06_relationships
cd 06_relationships
uv add sqlalchemy
```

Then include ruff into the `pyproject.toml`:

```toml
[tool.ruff]
# Set the maximum line length to 80
line-length = 80

[tool.ruff.lint]
# # Add the `line-too-long` rule to the enforced rule set.
# extend-select = ["E501"]
ignore = ["T201"] # Allow print statements

select = ["ALL"]
```

Then update the virtual env in your IDE, so that it matches the uv one.

To run the examples type:

```python
uv run <example_prog>.py
```
