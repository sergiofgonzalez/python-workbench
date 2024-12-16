# Error management and propagation in action


## Description

Write a function with the following signature:

```python
async def read_json(filename, cb) -> None
```

The function must use continuation passing style to unmarshal de contents of the file.

The functiom implementation must deal with errors found while opening the file and while parsing the contents of the file and must use continuation-passing style to communicate the result.

+ In v1 we use the regular blocking file read operation.
+ In v2, we still use the regular blocking file read, but on a separate thread using `to_thread`.
+ In v3, we use aiofiles to use a non-blocking file read operation.
+ In v4, a function factory in introduced to illustrate how to parameterize the callback function with custom arguments. This let us illustrate errors raised in the done callback.
+ In v5, a global exception handler is set to pick up exceptions raised in the callbacks. This is a sort of a last resort.
