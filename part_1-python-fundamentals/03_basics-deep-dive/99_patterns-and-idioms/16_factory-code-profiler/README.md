# Using the Factory pattern: a simple code profiler

Build a code profiler as an object with the following methods:
+ `start()` &mdash; triggers the start of a profiling session.
+ `end()` &mdash; finalizes the session and logs its execution time in the terminal.

The profiler must be automatically deactivated when `PY_ENV=production`.

## Testing the project

If you type:

```bash
uv run main.py 2025
```

you'll get the results with the profiler activated, but if you do:

```bash
PY_ENV=production uv run main.py 2025
```

you won't see any message.