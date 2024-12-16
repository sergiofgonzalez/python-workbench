# Observer pattern in Python: sync implementation

## Program description

Write a function that accepts a list of files and a regex. The function returns an event emitter so that consumers can register listeners that will get notified when the corresponding regex is found in a file.

This is information about the events that will be produced:
+ `"fileread"`: when a file is being read
+ `"found"`: when a match is found
+ `"error"`: when an error is found while the file is being read

In this project, we use a sync implementation of the observer pattern.

## Implementation details

+ v0: first implementation of the `EventEmitter` class to validate its basic functionality: register events, fire events, and remove listeners.
+ v1: the implementation of the `find_regex` function.