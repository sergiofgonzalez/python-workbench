# sync and async in Python
> demonstrates sync and async programming in Python

## Notes

There are two programs:

+ `syncmain.py` &mdash; a program in which a function involving a three-second sleep is invoked, and right afterwards another function is called. You should see a three second sleep between what is displayed in the first function and the second.

+ `asyncmain.py` &mdash; the same program but using async functions. You should see that both functions are executed in succession with no delay, and then the system sleeps for three seconds until it finishes.