# Async, Concurrency, and Starlette Tour

## Starlette

[Starlette](https://github.com/encode/starlette) is a lightweight ASGI framework/toolkit ideal for building async web services in Python.

It can be used as a web framework in its own right, or as a framework (as FastAPI does). Much of FastAPI's web code is based on Starlette.

| NOTE: |
| :---- |
| Flask takes a similar approach, using [Werkzeug](https://github.com/pallets/werkzeug/) package as the underlying platform. |

Starlette handles all the usual HTTP request parsing and response generation, but its most important feature is its support for modern Python asynchronous web standard: Asynchronous Server Gateway Interface (ASGI). The asynchronous approach is very conducive to web apps that very frequently interact with databases, files, network, etc.

## Types of Concurrency

This section discusses the multiple ways in which concurrency can be implemented.


### Distributed and Parallel computing

In parallel computing, a task is spread across multiple dedicated CPUs at the same time. This is common in CPU intensive operations like ML and graphic apps.


### Operating System Processes

An OS schedules resources: memory, CPUs, devices, networks, etc. Every program that it runs executes its code in one or more processes. The OS provides each process with managed, protected access to resources, including the CPU.

Most system uses *preemptive process scheduling*, that does not allow any process to hog the CPU, memory, or any other resource. The OS is in charge of suspending and resuming processes.

From the developer perspective, there's not much that you can do to change it. The usual solution is to use multiple processes and let the OS manage them (using the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) module).

Multiprocessing is recommended for CPU bound tasks.


### Operating System Threads

As a developer, you can also run threads of control within a single process. Python also provides a [threading](https://docs.python.org/3/library/threading.html) package to manage those.

Threads are recommended when your program is I/O bound, which is the case in web applications. However, programming with threads is tricky and can cause errors that are very difficult to find.

| NOTE: |
| :---- |
| Traditionally, working with multiprocesses and threading in Python was hard. A more recent package [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) is a higher-level interface that makes both easier to use. |

### Green Threads

Green threads is a *cooperative* (as oppose to *preemptive*) similar to OS threads but that run in the user space (your program) rather than in the OS kernel.

They work by monkey-patching standard Python functions to make concurrent code look like normal sequential code that would give up control when they are blocked by I/O operations.

Green threads are lighter than OS threads, which in turn are lighter than OS processes.

A prominent Python packages in this area are [gevent](https://github.com/gevent/gevent).

### Callbacks

Callbacks is another mechanism in which you write functions and associate them with an event (such as a mouse-click, key-press, or time-based event).

The Python package [Twisted](https://github.com/twisted/twisted) lets you use callbacks in Python.

### Python Generators

While Python code usually executes code sequentially, a generator function lets you stop and return from any point and get back to that point later.

```python
"""Simple example illustrating generators"""


def get_lines():
    yield "line 1"
    yield "line 2"
    yield "line 3"


for line in get_lines():
    print(line)
```

Any function containing `yield` is a generator function.

Note that a generator function can only be invoked in the context of an iteration (such as `for ... in`), but we see that Python keeps track of where it was executing to continue with the iteration.

This ability to go back into the middle of a function and resume execution is what is used for `async` and `await`.

### Python async, await, and asyncio

Python's [`asyncio`](https://docs.python.org/3/library/asyncio.html) had been introduced into the standard library over varios releases, and since Python 3.7, the `async` and `await` terms became reserved keywords.

```python
import asyncio


async def q():
    print("Question?")
    await asyncio.sleep(3)


async def a():
    print("Answer!")


async def main():
    await asyncio.gather(q(), a())


if __name__ == "__main__":
    asyncio.run(main())
```

Note that all the functions use `async def` instead of plain `def`, that we're using `await` to wait for async code to complete and that the functions are invoked using `asyncio.gather()`. Also, the main function uses `asyncio.run()` to execute the main program.

Note also that `asyncio.sleep()` releases the execution control to Python, so that it can execute `a()`.

The example uses `asyncio.sleep()` to simulate an I/O operation that will take a while.

You must put `await` in front of a function that might spend most of its time waiting, and that function needs to have `async` before its `def`.

When you define a function with `async def`, its caller must put `await` before calling it, and the caller itself must be declared `async def`, and its caller must await it, ... and so on all the way up.

| NOTE: |
| :---- |
| The use of `async` and `await` on their own don't make the code run faster. You will only get better performance when used to avoid long waits for I/O operations. |

## FastAPI and Async

Because web servers spend a lot of time waiting, performance can be increased by applying concurrency techniques.

FastAPI in particular do so by supporting async code via Starlette's ASGI support.

The following snippet illustrates how to use async/await on a FastAPI app.

```python
import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
async def greet():
    await asyncio.sleep(3)  # simulates 3 sec delay to retrieve message from db
    return "Hello, async FastAPI!"

```

From a single user perspective, there's not much of a difference from the sync counterpart. However, when using async/await you will be releasing the control back to the web server so that it can handle other requests while you wait.

Note also that when using FastAPI the `greet()` function will receive control without you having to use `await` anywhere. You will only be responsible for including `await` in the calls you'll make to other functions in the service or data layer that do async processing.

## Using Starlette Directly

FastAPI doesn't expose Starlette as much as it exposes Pydantic. However, in certain situations you might need to use it directly.

For example, in [part i](../../part-i-python-apis/) we saw use the following example:

```python
from starlette import status
from starlette.responses import Response
...

@app.delete("/orders/{order_id}")
def delete_order(order_id: UUID):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```
