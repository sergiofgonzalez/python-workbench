# Patterns and idioms
> assorted collection of notes and examples on patterns and idioms implemented in Python

## Monkey patching

The techniques in which we mutate an object by reassigning some of their properties or methods with custom code is called monkey patching.

This technique might come in handy when we need to alter the behavior of an object, especially in the context of tests, etc.

## The Callback pattern

Callbacks are functions that are passed as arguments to other functions and invoked to propagate the result of an operation. In the asynchronous world, they replace the use of the `return` instruction.

Python is well suited to work with callbacks, because functions are first-class citizens &mdash; they can be assigned to variables, passed as arguments to functions, returned from another function, ... &mdash; and the language supports the concept of **closures** so that functions created in that way can reference the environment in which they were created, no matter when the callback is invoked (even when the function in which they were defined gets out of scope).

### The continuation-passing style (CPS)
In functional programming, the way of propagating the result of an operation by invoking a callback that is passed as an argument to another function is known as **continuation-passing style (CPS)**.

This concept is not only associated to async operations &mdash; the style only states that the result of an operation is propagated by passing it to another function instead of directly returning the result to the caller.

#### Synchronous CPS

The following code illustrates a function that sums the arguments received using a *direct style*. This is the usual style used in regular Python:

```python
def add(a, b):
  return a + b
```

By contrast, the following block uses the *continuation-passing style*:

```python
def add(a, b, cb):
  cb(a + b)
```

Thus, invoking the function requires something like:

```python
add(2, 3, lambda result: print(f"The result is {result}."))
```

Note that the `add()` function itself doesn't return anything. It is callback the one that can do something with the result.

| EXAMPLE: |
| :------- |
| See [02: Sync CPS](02_sync-cps/README.md) for a runnable example. |

#### Asynchronous CPS

Async CPS in Python is not as common as in JavaScript, because of the improved Developer experience (*DX*) that coroutines and async/await provide.

However, you can find it useful in certain scenarios such as when starting a socket server, where you need to provide a callback that will be invoked async as soon as a client connects.

Callbacks can also be registered when working with `asyncio.Task`'s and `asyncio.Future`'s. Those are sync functions that will be invoked as soon as the task/future has completed either successfully or unsuccessfully:

```python
def when_done_cb(task: asyncio.Task) -> None:
    if not task.cancelled():
        print(f"Task completed: {task.result()}")
    else:
        print("For some reason the task was cancelled.")


async def add(a: float, b: float) -> float:
    await asyncio.sleep(0.1)
    return a + b


async def main() -> None:
    add_task = asyncio.create_task(add(2, 3))
    add_task.add_done_callback(when_done_cb)
    if not add_task.done():
        await add_task

if __name__ == "__main__":
    asyncio.run(main())
```

A `Task` is an object that schedules and independently runs a coroutine. That is, a task *wraps* a coroutine, schedules it for execution, and provides an interface to interact with it.

When you create a `Task` with `asyncio.create_task()`, the wrapped coroutine is automatically scheduled for execution without you needing to wait for it. Note that this doesn't mean it will run immediately. The event loop needs to pick up that task, which may not happen if the event loop is blocked by another task. It might also happen that the program finishes before the event loop has the chance to pick up the task. Because of that, it's quite common to see:

```python
if not task.done():
    await task
```

That idiom will ensure that the event loop picks up the task if it hasn't done that yet. As mentioned earlier, if you fail to do so, the task might not get scheduled, or might get cancelled before having had the chance to complete the execution.

| EXAMPLE: |
| :------- |
| See [03: Async CPS](03_async-cps/) for a runnable example. |

##### Notes on Task's lifecycle and interface

Lifecycle of tasks require some care, but the task interface will help you handle a task state correctly:

+ If a task fails while executing, the exception will be raised while awaiting for the task.

+ You can check if a task has completed its execution, and therefore is no longer eligible to be picked up by the event loop using `task.done()`.

+ You can check if the task was picked up by the event loop, but at some point, some other coroutine cancelled the task using `task.cancelled()`. A cancelled task is also done.

+ You can check the result of a task using `task.result()`. This should be called only when a task is done and not cancelled. Calling `task.result()` on a task not done raises an `InvalidStateError`. Calling `task.result()` on a cancelled task raises a `CancelledError`. If the task did not finish successfully, calling `task.result()` will re-raise the exception.

+ You can check the exception raised while executing a task calling `task.exception()`.

+ A task can be effectively cancelled using `was_cancelled = task.cancel()`. This method returns `True` if the task was cancelled, `False` otherwise.

All these complexities can be dealt with using the following code template:

```python
# Schedule the task for execution
task = asyncio.create_task(coro(a, b, c))
...
# Ensure event loop completes the execution of the task
if not task.done():
    try:
        await task
    except Exception as e:
        # Exception failed deal with the exception here
elif not task.cancelled():
    exception = task.exception()
    if not exception:
        # All went well, we can get the result
        value = task.result():
    else:
        # exception raised, we can get the exception for further processing
else:
  # Deal with the cancellation of the task
```


Note that:
+ you can register as many done callbacks as you want using `task.add_done_callback(when_done)`.

+ you can deregister a previously registered callback using `remove_done_callback()`.

Additionally, you can give the task a friendly name when using `asyncio.create_task()` or using `task.set_name()`. This name van be retrieved using `task.get_name()`.

### Non-CPS callbacks

It must be noted that the presence of a callback argument does not always mean that continuous-passing style is being used.

For example, the signature of the `map()` function is:

```python
map(function, iterable, *iterables)
```

This function returns an iterator that applies `function` to every item of `iterable`, yielding the results:

```python
nums = list(range(11))
double_nums = map(lambda x: x * 2, nums)
```

### Dealing with errors in CPS scenarios

See [05: CPS Error management](05_cps-err-management/) for an example illustrating how to deal with errors when using CPS.

## The Observer pattern

The **Observer** pattern is a fundamental pattern in the world of async programming, and a perfect way for modeling reactive applications that respond to events.

> The **Observer** pattern defines an object (called *subject*) that can notify a set of *observers* (sometimes called *listeners*) when a change in state occurs.

In traditional OOP, the **Observer** pattern requires interfaces, concrete classes, and a hierarcy. In some programming languages such as Node.js, there are core classes that allows you to register one or more functions (or listeners) which will be invoked when a particular event is fired.

![Observer pattern](pics/01_observer-pattern.png)

As an example, Node.js features an `EventEmitter` class with the following methods:
+ `on(event, listener)`: register a new listener (function) for the given event type (string).
+ `once(event, listener)`: register a new listener that will be removed after the given event is fired for the first time.
+ `emit(event, [arg1], [arg2], ...)`: produces a new event passing the optional arguments `arg1`, `arg2`, etc., to the registered listeners.
+ `removeListener(event, listener)`: removes a listener for the specified event type.

In Node.js, all those methods return the `EventEmitter` instance, to allow method chaining.

The listeners, are regular functions that receive the optional arguments `arg1`, `arg2`, etc.