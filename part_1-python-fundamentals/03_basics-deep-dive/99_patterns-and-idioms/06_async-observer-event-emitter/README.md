# Observer pattern in Python
> a naive implementation of the observer pattern in Python, following the interface defined in Node.js

## Program description

Write a function that accepts a list of files and a regex. The function returns an event emitter so that consumers can register listeners that will get notified when the corresponding regex is found in a file.

This is information about the events that will be produced:
+ `"fileread"`: when a file is being read
+ `"found"`: when a match is found
+ `"error"`: when an error is found while the file is being read


## Implementations

+ v0: we explore `asyncio.Event` as a synchronization primitive.
+ v1: we keep exploring to see how by subclassing `Event` we can label events with a name.
+ v2: illustrates that if you await for a listener whose event is never triggered the program does not finish.
+ v3: the first attempt at implementing the Event Emitter. It requires invoking a method to start the process. Do we really need asyncio?
+ v4: the same program without using `asyncio.gather()`. It works! (but I don't know exactly why! 🤔)
+ v5: wrapping up the implementation to support passing parameters and establishing custom callbacks. I noticed that the way in which event parameters are passed is buggy, and the information gets overwritten.
+ v6: Adding the find_regex implementation, and wrapping it up, but had the same problem as above.
+ v7: the sync implementation, but using asyncio to have non-blocking I/O.
+ v8: the final implementation that allows for registering async callbacks.