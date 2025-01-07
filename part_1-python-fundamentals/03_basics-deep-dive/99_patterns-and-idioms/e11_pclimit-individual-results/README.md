# PCLimit: accessing the individual results

Use the newly developed `PCLimit` async context manager to illustrate that you can now get the individual results of `PCLimit.run()` invocations by reimplementing the example in which the async work is implemented using the following function:

```python
async def async_work() -> float:
    """Async piece of work to be handled by run()."""
    delay_seconds = random.uniform(0.5, 1.5)
    await asyncio.sleep(delay_seconds)
    return delay_seconds
```