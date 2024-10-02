# SQLAlchemy: Basics of connections and transactions
> basics such as creating an engine, getting a connection and executing a SQL statement using `text()` construct


## Setting up shop

```bash
uv init 01_getting-a-connection
cd 01_getting-a-connection
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

## Connecting DBeaver to a SQLite file on WSL

If you want to see the contents of the database using DBeaver, it's required that you change the connection string to file, and also make the file available in your Windows filesystem by way of copying.

First, you need to change the connection string:

```python
engine = create_engine("sqlite+pysqlite:///samples.db", echo=True)
```

Then make the file available in Win:

```bash
cp samples.db ~/win_downloads/
```

And then you can open that file in DBeaver.