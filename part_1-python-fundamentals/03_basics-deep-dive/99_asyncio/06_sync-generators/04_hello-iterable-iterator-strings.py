"""Iterating over built-in strings."""

from collections.abc import Iterator

s = "foobar"

# You can iterate over a string
for ch in s:
    print(ch)


# But a string is not an iterator (i.e., doesn't implement next())
try:
    next(s)
except Exception as e:
    print(f"Ooops: {type(e)}: {e}")

# But a string is iterable (i.e., implements __iter__ which returns an iterator
# or take indices)
my_iterator = iter(s)

print(next(my_iterator)) # f
print(next(my_iterator)) # o
print(next(my_iterator)) # o
