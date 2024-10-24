# Async programming in Python with `asyncio`
> notes from https://bbc.github.io/cloudfit-public-docs/

An async program takes one execution step at a time, as in a regular sync program, but in this case, the system may not wait for an execution step to be completed before moving on to the next one.

`asyncio` will not make your code multithreaded. It will not make multiple Python instructions in your program to execute at the same time, and will not let you to sidestep the [global interpreter lock](https://wiki.python.org/moin/GlobalInterpreterLock) (GIL) &mdash; a mutex that prevents multiple threads from executing Python bytecodes preventing race conditions.

When a program is IO-bound, it's pretty common for the CPU to spend a lot of time doing nothing at all because it is just waiting for some I/O to complete.

> `asyncio` is designed to allow you to structure your code so that when one piece of linerar single-threaded code (called *coroutine*) is waiting for something to happen another can take over and use the CPU.

## Subroutines and Coroutines

Most programming languages have functions/methos which follow what is called the *subroutine* calling model. In this model of calling each time a function is called execution moves to the start of that function, then continues until it reaches the end of that function (or a `return` statement), at which point execution moves back to the point immediately after the function call, any later calls to the function are independent calls which start again at the beginning.

There's an alternative model of code execution called the ***coroutine* calling model**. In this calling model there is a new way for the method/function called *coroutine* to move execution back to the caller: instead of returning, it can yield control. When the coroutine yields execution moves back to the point immediately after it was called, but future calls to the coroutine do not start again at the beginning, but instead, they continue from where the execution left off most recently.

The following diagrams illustrate both calling models:

![Subroutines vs. Coroutines](pics/subroutines-vs-coroutines.png)

Python had the capability to allow this execution model with their generators, but asyncio adds a new type of coroutine which allows for a more natural way to write code where execution can move around between coroutines when the current one gets blocked.

## Stacks and frames

Most OS and programming languages make use of an abstraction known as a stack machine. This mechanism is the one that allows you to call one piece of code from another.

Consider the following piece of Python code:

```python
def a_func(x):
    return x - 2

def main():
    some_value = 12
    some_other_value = a_func(some_value)

main()
```

When we begin executing this program, the code stack is initialized as an empty LIFO area of storage in memory, and the instruction pointer is initialized in the line `main()`:

![Execution: 001](pics/execution_001.svg)

In order to allow *function calling*, the stack machine mechanism does the following:
1. Adds a new frame to the stack. You can think of the frame as a data structure that will contain anything that is put on the stack after it.

2. Puts the return pointer on the stack. This is the address that tells the system where execution needs to be resumed after having called the function.

3. Updates the instruction pointer so that it points to the first executable line of the function being called (`def main()` in this case).

![Execution: 002](pics/execution_002.svg)

The first instruction in `main` is an assignment (`some_value = 12`):

1. The stack machine mechanism will store this local variable assignment on the stack, inside the stack frame for this function call.

2. The instruction pointer will be updated to point to the next execution statement.

![Execution: 003](pics/execution_003.svg)

The next instruction is another assignment, but the right value is a function call. As such, the interpreter will repeat the function call process seen before:

1. A new frame will be pushed to the top of the stack.

2. The address of the next instruction to be called inside `main` when the current function call is completed is pushed to the stack (`Return Point = 04`).

3. Because the function being called expects a parameter, this parameter will be pushed to the stack (`x = 12`).

4. It updates the instruction pointer so that the first line of the function `a_func` will be the next instruction to be executed:

![Execution: 004](pics/execution_004.svg)

The next instruction to be executed is `return x - 2`. This time the interpreter performs the process for returning from a function which is:

1. Pop the top frame from the stack, including everything in it.

2. Pushes the return value of the called function on the top of the stack.

3. Moves the execution (updates the instruction pointer) to the address that was in the frame recently popped (`Return Point = 04`).

![Execution: 005](pics/execution_005.svg)

And this finalizes the program.

This approach is followed in all traditional programming languages. In multithreaded programming it is still like this, but each thread features a separate stack so that multiple execution threads can perform function calling, etc.

## Event loops, tasks, and coroutines

In the asyncio world, we no longer have one stack per thread. Instead, each thread has an object called **Event Loop**. The event loop contains a list of objects called tasks. Each task maintains a single stack, and its own execution pointer.

At any one time the event loop can only have one Task actually executing (the fact that a processor can still do one thing at a time still remains), and the other tasks managed by the event loop are paused.

![Event Loop](pics/event-loop.svg)

The currently executing task will continue to execute exactly as if it were executing a function in a normal (sync) Python program, right up until it gets to a point where it would have to wait for something to happen before it can continue.

At that point, instead of waiting, the code in the Task yields control. Then, the event loop will pause the Task that was running and will be in charge of waking it up again at a future point once the thing it needs to wait for has happened.

The event loop can then select one of the other tasks it is managing and make it the active task. If none of the tasks are ready to continue (i.e., if all of them are waiting for a certain event to happen), the event loop will wait.

By using this mechanism, the CPU's time can be efficiently shared between different tasks, all of which are executing code capable of yielding like this when they would otherwise wait.

| NOTE: |
| :---- |
| As happens in JavaScript, an event loop cannot forcibly interrupt a coroutine that is currently executing. That is, a coroutine will keep executing until it yields control. |

This execution pattern, where the code control moves back and forth between different tasks, waking them back up at the point where they left off is called **coroutine calling**, and this is what `asyncio` provides to Python programming.

## Awaitables, Tasks, and Futures

### Writing asynchronous code

The keyword `async def` is the most basic tool in the toolkit of an async programmer in Python. It is used to declare an **async coroutine function** pretty much in the same way `def` is used for sync functions:

```python
def example_function(a, b):
    ...

async def example_coroutine_function(a, b):
    ...
```

| NOTE: |
| :---- |
| Asynchronous Python code can only be included inside a suitable context that allows it, which almost always means inside a coroutine function defined using `async def`. |
| Within async Python code you can use any of the regular Python code &mdash; nothing is disallowed (although certain things are discouraged). |
| There are certain keywords that can only be used within async code: `await`, `async with` and `async for`. |

The Python `def` keyword creates a callable object with a name. When the object is called, the code block of the function is run:

```python
def example_function(a, b, c):
    ...

r = example_function(1, 2, 3)
```

The Python `async def` keyword creates a callable object with a name. When the object is called, the code block of the function **is not run**.

That is, the following code define a callable object named `example_coroutine_function` with three parameters:

```python
async def example_coroutine_function(a, b, c):
    ...
```

The syntax to invoke it is deceptively similar to the one used with regular functions:

```python
r = example_coroutine_function(1, 2, 3)
```

However, that will not cause the coroutine code block to be run. Instead, an object of class `Coroutine` is created and assigned to `r`. To make the code block actually run you need to make use of one of the facilities that `asyncio` provides for running a coroutine. Most commonly, this is the `await` keyword.

When using types, you will use:

```python
async def example_coroutine_function(a: A, b: B) -> C
    ...
```

This defines `example_coroutine_function` as a callable that takes two parameters of type `A` and `B` and returns an object of type `Coroutine[Any, Any, C]`, where the first parameter of the `Coroutine` type indicates the type of the values that the coroutine will pass to the event loop whenever it yields, and the second represent the type of the values that the event loop will pass to the coroutine whenever it is reawakened. It's not usual that you'll need to refer to those explicitly.

### The `await` keyword and awaitables

The `await` keyword is used as an expression which takes a single parameter and returns a value. It can only be used inside async code blocks (i.e., in the code block of an `async def` statement defining a coroutine function):

```python
r = await a
```

What happens when this `await` statement is executed depends upon what the object `a` is.

A coroutine object is *"awaitable"* (it can be used in an `await` statement).

Recall that when you are executing async code you are always doing so in the context of a *"Task"*, which is an object maintained by the Event Loop., and that each *Task* has its own call stack.

The first time a *Coroutine* object is awaited the code block inside its definition is executed in the current Task, with its new code context added to the top of the call stack for this Task, just like a normal function call.

When the code block reaches its end (or otherwise returns), then execution moves back to the `await` statement that called it. The return value of the `await` statement is the valur returned by the code block. If a Coroutine object is awaited a second time this raises an exception.

| NOTE: |
| :---- |
| You can think of awaiting a Coroutine object very much like calling a function, with the notable difference that the Coroutine's object can contain async code, and so can pause the current task during running, which a regular function's code block cannot. |

There are three types of awaitable objects:
+ A Coroutine object. When awaited, it will execute the code block of the coroutine in the current Task. The `await` statement will return the value returned by the coroutine's code block.

+ Any object of class `asyncio.Future` which when awaited causes the current Task to be paused until a specific condition occurs.

+ An object which implements the magic method `__await__`, in which case what happens when it is awaited is defined by that method.

| NOTE: |
| :---- |
| There is an abstract class `Awaitable` which is generic, so that `Awaitable[R]` for some type `R` means "anything which is awaitable, and when used in an `await` statement will return something of type `R`". |

A currently executing Task cannot be paused by any means other than awaiting a future (or a custom awaitable object that behaves like one), which can only happen inside async code.

Thus, any `await` statement might cause your current task to pause, but it is not guaranteed to. Conversely, any statement which is not an `await` statement (or `async for` or `async with`) cannot cause your current Task to be paused.

Race conditions in async code are limited in this execution mode, but are not entirely eliminated.

Consider the following code block:

```python
import asyncio

async def get_some_values_from_io():
    # some I/O associated code which returns a list of values
    ...

vals = []

async def fetcher():
    while True:
        io_vals = await get_some_values_from_io()

        for val in io_vals:
            vals.append(val)

async def monitor():
    while True:
        print(len(vals))

    await asyncio.sleep(1)

async def main():
    t1 = asyncio.create_task(fetcher())
    t2 = asyncio.create_task(monitor())
    await asyncio.gather(t1, t2)

asyncio.run(main())
```

In the example above, even when both `fetcher()` and `monitor()` access the global variable `vals` they do so in two tasks that are running in the same event loop. This means that the `print()` statement in `monitor()` can only be executed when `fetcher()` is asleep waiting for I/O.

This is guaranteed because there are not `await` statements involved.

Note also that the `create_task` is superfluous in the example above. It would have been possible to do:

```python
await asyncio.gather(fetcher(), monitor())
```

### Futures

A `Future` object is a type of awaitable. Unlike a coroutine object, when a future is awaited it does not cause a code of block to be executed. Instead, a future object can be thought of as representing some process that is ongoing elsewhere and hich may or may not yet be finished.

When you await a future the following happens:

+ If the process the future represents has finished and returned a value, then the await statement immediately returns that value.

+ If the process the future represents has finished and raised and exception then the await statement immediately raises that exception.

+ If the process the future represents has not yet finished, then the current Task is paused until the process has finished. Once it is finished it behaves as described in the first points.

All `Future` objects have the following sync interface (in addition to being awaitable):

+ `f.done()` &mdash; returns `True` if the process the `Future` represents has finished.

+ `f.exception()` &mdash; raises an `asyncio.InvalidStateError` exception if the process has not yet finished. If the process has finished it returns the exception it raised, or `None`if it terminated without raising.

+ `f.result()` &mdash; raises an `asyncio.InvalidStateError` exception if the process has not yet finished. If the process has finished it raises the exception it raised (if any), or returns the value it returned if it finished without raising.

A future becoming done is a one-time occurrence.

| NOTE: |
| :---- |
| A Coroutine's code will not be executed until it is awaited. A Future represents something that is executing anyway, and simply allows your code to wait for it to finish, check if it has finished, and fetch the result it has. |

You won't create your own futures very often, unless implementing new libraries that extend `asyncio`. If you do need to create your own future directly you can do:

```python
f = asyncio.get_running_loop().create_future()
```

A variable representing a `Future` can be annotated with `asyncio.Future`. If the future's result is of a specific type `R` you can do:

```python
f: asyncio.Future[R]
```

### Tasks

Each event loop manages a number of tasks, and every coroutine that is executing is doing so inside a task.

A task is created with a block of sync code as the following:

```python
async def example_coroutine_function():
    ...

t = asyncio.create_task(example_coroutine_function())
```

`create_task()` takes a coroutine object and returns a `Task` object that inherits from `Future`.

The call creates the task inside the event loop for the current thread, and starts the task executing at the beginning of the coroutine's code block. The returned future will be marked as `done()` only when the task has finished execution. The return value of the coroutine's code block is the `result()`, which will be stored in the future object when it is finished.

Creating a task to wrap a coroutine is a sync call, and therefore can be done inside a sync or async code block.

+ If done in an async block, the event loop will be already running. It will make the new task active as soon as it gets the chance.

+ If done in a sync block, it might be that the event loop is not yet running. According to the Python documentation, you should avoid creating a task from sync code.

That is, if you need to call a single piece of async code in a sync code block, you should use `asyncio.run()`.

### Running async programs

Since Python 3.10, it is unlikely that you'd need to interact with the event loop unless you're developing a low-level async lib. Instead you'll use `asyncio.run()` for all the async related operations.

`asyncio.run(coro)` will run `coro`, and return the result. It will always start a new event loop, and it cannot be called when the event loop of the current thread is already running.

This means that there are a couple of ways to run your async code:

```python
import asyncio

async def get_data_from_io():
    ...

async def process_data(data):
    ...

async def main():
    while true:
        data = await get_data_from_io()
        await process_data(data)

asyncio.run(main())
```

The second way is to wrap each coroutine call in a separate `run` command.

```python
import asyncio

async def get_data_from_io():
    ...

async def process_data(data):
    ...

def main():
    while true:
        data = asyncio.run(get_data_from_io())
        asyncio.run(process_data(data))

main()
```

| NOTE: |
| :---- |
| The seconda way is less common, although it might be useful in certain circumstances. |

It must be notes that these examples do not benefit from the ability of async code to work on multiple tasks concurrently, as you're immediately awaiting the result of the first coroutine object before executing the second, and then awaiting until the second has completed.

### How to yield control to the event loop

Occasionally, you might want to yield control to the event loop so that other task can be made active. This is not very common, as normally you'd prefer the control to be yielded automatically when you await a future returned by some underlying library that is doing some type of I/O.

In those rare cases, you can do:

```python
await asyncio.sleep(0)
```

`asyncio.sleep(num_seconds)` taskes a single parameter and returns a future which is not marked done, but will be when the specified number of seconds have passed. Specifying `0` as the number of seconds will make the current task to stop executing, giving a chance to the event loop to make some other task active. Specifying a number > 0 guarantess that your task won't be awakened before those number of seconds have passed.

### Summary: awaitables, coroutines, futures, and tasks

The following diagram describes the different awaitable objects available in the asyncio library:

![asyncio awaitables](pics/awaitables_coroutines_futures_tasks.png)

With these concepts in place, you can start writing your first async program taking advantage of multiple tasks running concurrently within an event loop: see [01: Hello, asyncio!](01_hello-asyncio/).

## Async context managers and async iterators

Async context managers and async iterators are two additional features provided by asyncio that are widely used in library interfaces. Understanding them are very much needed to make proper use of the async programming paradigm in Python.

### Reviewing (sync) context managers

Context managers allow you to allocate and release resources precisely when you want to. Python provides the `with` statement that you can use to benefit from context managers with a succinct and very expressive syntax:

```python
with open("my_file.txt", "w") as opened_file:
    opened_file.write("Hello, world!")
```

The code above:
+ Opens the file `my_file.txt` in write mode and binds it to the `opened_file` variable.
+ Writes some text on the opened file.
+ Automatically closes the file when the `with` code block is reached.
+ If an error occurs while writing the data to the file, or while opening it, the file will be automatically closed.

That is, the code above is equivalent to:

```python
file = open("some_file", "w")
try:
    file.write("Hello!")
finally:
    file.close()
```

Context managers are not things left out to low-level library developers &mdash; they can be easily implemented by you when you need to face a use case requiring some setup and teardown on an resource.

One of the possible implementation approaches relies on classes:

```python
class File:
    def __init__(self, file_name, method):
        self.file_name = file_name
        self.method = method
        self.file_obj = None

    def __enter__(self):
        self.file_obj = open(self.file_name, self.method)

    def __exit__(self, type, value, traceback):
        self.file_obj.close()
```

With that code in place, you can enable a client code like the following:

```python
with File("my_file.txt") as opened_file:
    opened_file.write("Hello, world!")
```

Note the signature of the `__exit__` method. Those parameters are required by every `__exit__` method which is part of a Context Manager. They are the type, the actual value, and the associated traceback of any exception that is raised within the context manager block.

When dealing with exceptions you should also be aware of the protocol:
+ if anything other than `True` is returned, this means that the exception could not be handled, and the exception will be propagated.
+ if `True` is returned, it is assumed that the exception was properly handled and won't be propagated.

| EXAMPLE: |
| :------- |
| See [02_sync-context-managers](02_sync-context-managers/) for a runnable example. |

It is also possible to implement a context manager with a generator:


### Async context managers

Async context managers are an extension of the concept of context managers to work in an async environment. They are used in many asyncio-based library interfaces.

An async context manager is an object which can be used in an `async with` statement:

```python
async with FlowProvider(store_url) as provider:
    async with provider.open_read(flow_id, config=config) as reader:
        frames = await reader.read(720, count=480)

        # ...do things with reader...
    # ...do things with provider...
# ...do things with frames...
```

This is what happens in the example above:
1. Resource acquisition is performed for `FlowProvider` and the result is bound to `provider`.
2. Resource acquisition is performed for `provider.open_read` and the result is bound to `reader`.
3. Inside the async context manager, there is a code block in which `reader` is available to use. `await reader.read()` is used to obtain `frames`.
4. Within the same block other actions on `provider`, `reader`, or `frames` can be performed while they're still in a stable state.
5. When the innermost async code block end is reached, tidy-up is performed for the `reader`. This object will no longer be safe to use as the resource deallocation will be done.
6. When the outermost async code block end is reached, tidy-up is done for the `provider`. This object will no longer be safe to use as the resource deallocation will be done.
7. Outside the context manager `frames` is still accessible and safe to use (as it holds their values).

Thus, async context managers and the regular ones share the same principle, with the only difference being that the setup and teardown performed on entry and exit in async context managers are performed by awaiting async coroutines. That is, there are hidden `await` statements when we set up and tear down the `provider` and `reader` objects.

Additionally, `async with ...` can only be used in coroutines.

Technically, `async with` is just syntactic sugar for more complex Python code:

```python
# simple Python async with
async with AsyncCM as ctx:
    ...

# is the same as:
ctx = await AsyncCM.__aenter__()
try:
    ...
except Exception as e:
    if not await AsyncCM.__aexit__(type(e), e, e.__traceback__):
        raise e
else:
    await AsyncCM.__aexit__(None, None, None)
```

That is, you to implement an async context manager you just need to implement the methods:

```python
async def __aenter__(self):
    ...

async def __aexit__(self, exc_t, exc_v, exc_tb):
    ...
```

Note that:
+ the return value of `__aenter__` may be anything. Whatever value it returns is the object which will be bound by any `as` clause used in the `async with` statement.

+ if the code block of the `async with` reaches its end without an exception, then `__aexit__` will be called with the three parameters set to `None` and its returned value will be ignored.

+ if the code block of the `async with` raises an exception, `__aexit__` will be called with the type of the exception, the exception object itself, and a traceback associated with the exception. If it returns `True` (or *truthy*), the system will assume that the exception has been handled and corrected for, and will not propagate it any further. If it returns `False`, `None`, anything that evaluates to *falsy*, or nothing at all, the exception will continue to propagate.

| NOTE: |
| :---- |
| This behavior mirrors how regular context managers work. |

In modern versions of Python, you can also define your own async context manager with the `@asynccontextmanager` decorator:

```python
@asynccontextmanager
async def ExampleAsyncCM(param_a, param_b):
    # ...perform the setup that would go in __aenter__ ...

    yield obj

    # ...perform teardown that would go in __aexit__
```

| EXAMPLE: |
| :------- |
| See [04: async context manager](04_async-context-manager/) and [05: async context manageer generator](05_async-context-manager-generator/) for a runnable example. |


### Async Iterators

Async iterators are a natural async analogue to regular iterators. Let's start by reviewing what an sync iterator is.

#### Reviewing (sync) iterators

An iterator is a design pattern that enables a programmer to traverse a container such as a list.

In Python, there are three related concepts:
+ Iterable
+ Iterator
+ Iteration

An `Iterable` is any object which implements and `__iter__` or `__getitem__` method that returns an iterator or can take indexes. That is, an `Iterable` is any object that provides an **iterator**.

In turn, and **iterator** is a Python object that implements the `__next__` method.

Iteration is the process of taking an item from a container (e.g., a list). When we use a loop to loop over something it is called iteration.

#### Back to Async Iterator

An iterable represents a source of data which can be looped over with a `for` loop. Thus, a an async iterable represents a source of data which can be looped over with an `async for` loop:

```python
async for value in reader.get_values():
    # do something with value
```

In the example above, `reader.get_values()` returns an async iterable object, and the loop draws elements from it one by one, assigning each to the local variable `value` within the loop body.

The only difference from a regular loop, is that the method to extract the next element from the async iterator that derived from the iterable is an async coroutine method, and its output is awaited.

In reality, the `async for` construct is syntactic sugar:

```python
# async for construct
async for a in async_iterable:
    await do_something(a)

# equivalent
it = async_iterable.__aiter__()
while True:
    try:
        a = await anext(it)
    except StopAsyncIteration:
        break

    await do_something(a)
```

The `async for` loop can only be used in a context where async code is permitted (i.e., inside a coroutine).

An async iterator comes in handy when representing a remote resource which requires some time consuming I/O to be performed each time another object is pulled from it.

Note that async iterator could be designed with an optimized loading strategy that acts to load resources in the background (by adding tasks to the runloop) and only pauses the current task when an object is needed if that object hasn't been loaded yet.

To implement a custom async iterable you just need to implement the magic method:

```python
def __aiter__(self):
    ...
```

| NOTE: |
| :---- |
| The method `__aiter__(self)` is not a coroutine. |

Implementing an async iterator is also easy:

```python
def __aiter__(self):
    return self

async def __anext__(self):
    ...
```

Note that `__anext__` should be a coroutine method which returns the next item in the iterator each time it is awaited.

As it happens with sync iterables and iterators, generators makes our life easier.

### Async Generators

Let's start by reviewing their sync counterparts:

#### Sync Generators

Generators are iterators, that is, objects that implement the `__next__` method, but you can only iterate over them once.

Generators generate values on the fly, and you can iterate over generators by either using a `for` loop, or by passing them to any function or construct that iterates.

Most of the time, generators are implemented as functions that `yield` rather than return values:

```python
def generator_fn():
    for i in range(10):
        yield i

for item in generator_fn():
    print(item)
```

Generators come in handy when you need to calculate a large set of results and you don't want to allocate the memory for all the results, and instead, can compute one by one on demand.

One such example is calculating the numbers of the Fibonacci sequence:

```python
def fibonacci(n: int):
    """Return an iterator over the first n numbers of the Fibonacci sequence."""
    a = 1
    b = 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Print the first 10 numbers of the Fibonacci sequence
for i in fibonacci(10):
    print(i)
```

Using a generator is much more efficient than the alternative implementation that materializes the whole sequence (especially for large numbers of n).

A generator is an iterator, that is, it implements the magic method `__next__` behind the scenes, which we can invoke as consumers using `next()`.

```python
def generator_fn() -> Iterator[int]:
    for i in range(3):
        yield i


gen = generator_fn()

print(next(gen)) # 0
print(next(gen)) # 1
print(next(gen)) # 2

# Oops!
print(next(gen)) # StopIteration error
```

Some built-in data type support iteration:

```python
s = "foobar"

# You can iterate over a string
for ch in s:
    print(ch)
```

But a string isn't an iterator, that is, it doesn't implement `next()`:

```python
s = "foobar"

next(s) # TypeError: str object is not an iterator
```

But because it is an iterable, it implements the `__iter__()` method that either returns an iterator or take indices. In any case, we can get an iterator by calling `iter()` on an iterable object:

```python
s = "foobar"

my_iterator = iter(s)

print(next(my_iterator)) # f
print(next(my_iterator)) # o
print(next(my_iterator)) # o
```

#### Back to async generators

An async generator is a shorthand method for defining an async iterator. An async generator is a coroutine that must contain at least one use of the keyword `yield`:

```python
async def async_generator_fn(param):
    # ... do something
    yield something
    # ... do other stuff
    yield some_other_something
    # ... more stuff
```

Note that an async generator is a sync method which returns an async generator object, and as such, it cannot be awaited:

```python
async def async_gen(param):
    yield 3

# This will raise an exception
r = await async_gen()
```

The easiest way to consume an async generator is with the `async for` construct:

```python
async for r in async_gen():
    print(r)
```

#### Advanced Async Generators

A `yield` statement inside a generator can be made to return a value as well as taking one:

```python
async def advanced_gen(y):
    for i in range(10):
        x = await do_something(y)
        y = yield x
```

But you can't make use of that capability with an `async for` loop &mdash; you need to be more explicit:

```python
it = advanced_generator(first_y)
x = await anext(it)

while True:
    y = await do_something_else(x)
    try:
        x = await it.asend(y)
    except StopAsyncIteration:
        break
```

The code above passes values back and forth between the generator and calling object each time it is called.

#### Async Comprehensions

A generator comprehension is a special type of syntax that lets you define generators in a much compact way.

For example, compare the two different ways of implementing a generator that lets you iterate over the squares of integer numbers from 0 to 9:

```python
# Generator
def gen_squares():
    for n in range(10):
        yield n * n

# Generator comprehension
squares = (x * x for x in range(10))
```

In the async world, this is also possible using the following syntax:

```python
it = (<async_expression> async for <variable> in <async_iterable> if <condition>)
```

Which is equivalent to:

```python
async def async_gen():
    async for <variable> in <async_iterable>:
        if <condition>:
            yield <async_expression>

it = async_gen()
```

## Library support
