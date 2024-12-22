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

| EXAMPLE: |
| :------- |
| See [07: synchronous observer (EventEmitter)](07_sync-observer-event-emitter/) for a synchronous implementation of the observer pattern, and [06: Async observer (EventEmitter)](06_async-observer-event-emitter/) for an async implementation and allows registering coroutines as callbacks.  |

### Making any object observable

It's not very common to find a *subject* object in the wild. Instead, the norm is to extend a class such as the `EventEmitter` of the previous section to inherit the capabilities of that class and ultimately making the custom class a factory of observable objects.

| EXAMPLE: |
| :------- |
| See [08: Observables](08_async-observables/) for a runnable example. |

### Observables and memory leaks

When subscribing to observables with a long life span, it is very important to unsubscribe our listeners/callbacks when they are no longer needed.

This will prevent memory leaks associated with chunks of memory that are kept even those will no longer be needed.

| NOTE: |
| :---- |
| In JavaScript in particular, where event managements are so prevalent, unreleased listeners are the main source of memory leaks. |

Consider the following example:

```python
long_str = "long string taking a lot of memory...."
emitter.register_listener("an_evt", lambda: print(long_str))
```

Because the listener function references `long_str`, it will not be reclaimed by the garbage collector unless the `emitter` itself is collected or we explicitly release the listener.

> A memory leak is a software defect whereby memory that is no longer needed is not released, causing the memory usage of an application to grow indefinitely.

As a precaution, Node.js keeps track of the number of listeners an `EventEmitter` controls, and warns the user when the limit is reached. Also, Node.js exposes a `once(event, listener)` which automatically unregisters a listener after the event is triggered for the first time. Note however, that if the corresponding event is never fired, `once()` will nevertheless create a memory leak.

### Caveats and additional notes

Python features an `Event` synchronization object in the `asyncio` package that is completely different in nature from the events we've used in the previous section. An `asyncio.Event` can be used to establish a waiter task that will be stopped until the event has been fired. The event won't carry additional information by default, and once fired, the rest of the logic will be executed:

```python
async def handle_evt(evt: asyncio.Event):
    # ... do stuff before waiting ...
    await event.wait()
    # ... do stuff after event fired
```

That approach complicates using an `asyncio.Event` to implement a generic Observer pattern.

By contrast, the `EventEmitter` works pretty much like the Node.js one, but it's not as robust, and many things should be considered.

> It is crucial that we never mix the sync and async approach in the same `EventEmitter`, and that you don't emit the same event type using a mix of sync and async code.

When events are emitted asynchronously, new listeners can be registered even after the task that produces the events because it is guaranteed that they will not be fired up until the next cycle of the event loop. This is not guaranteed for events emitted synchronously, and therefore, we need to register the listeners before we launch the task, or we will miss all the events.

+ Talk about mixing sync and async event (maybe emit should be async).
+ Try to find caveats
+ Not a good thing to mix sync and async, same with callbacks.

### Callbacks vs. EventEmitter (Observer pattern)

The difference between using callbacks and the observer pattern is mostly semantic:

+ Use a callback when a result must be returned in an asynchronous way.
+ Use events when there's a need to communicate that something has happened to external observers.

When deciding whether to use callbacks or events follow these rules:
+ Use events when you need to communicate different types of situations (e.g., `"fileread"`, `"complete"`, `"match"`...). Callbacks are not well prepared to handle different types of situations, and might require an extra argument to identify the event, making the API less elegant.

+ Use events when a situation can occur a multiple number of times, or may not occur at all. Callbacks are expected to be invoked exactly once, whether the operation is successful or not. If you're using callbacks for a situation that is repetitive in nature, reconsider if an event based approach would be more appropriate.

+ Use callbacks for an API that has to communicate a given result to exactly one interested party. If a given result should be communicated to more than one party, use events instead.

### Combining callbacks and events

In some circumstances, using an event-based approach in conjunction with callbacks gives us an extremeley powerful pattern.

> Using both a callback and an `EventEmitter` allows us to pass a result asynchronously using a callback, and at the same time providing a more detailed account on the status of the asynchronous processing using event.

For example:

```python
event_emitter = find_regex(search_str, callback)
```

This will allow the callback to process the whole list of matches, while the event emitter will be helpful to provide live feedback to the user while the scanning is in progress.

| EXAMPLE: |
| :------- |
| See [09: Mixing events and Callbacks](09_mixing-events-and-callbacks/) for a runnable example. |

### Exercises on events and callbacks

#### Exercise 1: [A simple event](e01_find-regex-simple-event/)

Modify the `FindRegex` class so that it emits an event when the find process starts, passing the list of input files as an argument to the event handler.

#### Exercise 2: [Ticker](e02_ticker/)

Write a function that accepts a number and a callback as the arguments. The function will return an `EventEmitter` that emits an event called `"tick"` every 50 milliseconds until the number of milliseconds is passed from the invocation of the function. The function will also call the callback when the number of milliseconds has passed, providing as the result the total count of `"tick"` events emitted.

Bonus: try to use `asyncio.sleep()` recursively.

#### Exercise 3: [A simple modification](e03_ticker-simple-modification/)

Modify the function from the previous exercise ([Ticker](e02_ticker/)) to emit a `"tick"` event immediately after the function is invoked.

#### Exercise 4: [Playing with errors](e04_ticker-playing-with-errors/)

Modify the function created in the previous exercise ([A simple modification](e03_ticker-simple-modification/)) to produce an error if the timestamp at the moment of a tick (including the one emitted at the beginning) is divisible by 5. Propagate the error using both the callback and the event emitter and handle the error correctly.

#### Exercise 5: [Identifying event/callback associated memory leaks]()

Create a program that creates a memory leak by subscribing to an event and never unsubscribing from it.

Identify the problem and fix it by unsubscribing.

Try to find a package like clinic but for Python to visually identify the memory leak.