# Concurrency and recursion caveats

When using limited parallel execution, you may face a deadlock if the level of concurrency is less than the required recursion depth needed to find a result. Create an async implementation of the `factorial()` function using work queues and illustrate that caveat.