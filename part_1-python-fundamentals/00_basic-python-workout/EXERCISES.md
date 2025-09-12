# Getting up to speed with simple projects
> distilled list of projects from [01_python-workout](01_python-workout.ipynb) notebook with solutions in [projects/](projects/)


## 01: Shakedown test

### 010: Hello, Python

Create a hello, world Python project to make sure that you have your environment correctly created by creating a hello world program using `uv`. Configure the project to use the latest stable Python version (e.g., 3.13.3 at the time of writing).


## 02: The basics

### 021: Hello, function

Create a simple function that calculates the square of a given number. Print the result of invoking the function.

### 022: Higher-order function

Create a function `add(x, y)` that sums up the numbers received as arguments, and a function `sub(x, y)` that subtracts those numbers.

Define the function `compute(x, y, op)` that receives as argument two numbers and a function such as `add()` and `sub()` and use it to perform some calculations.

### 023: Using functions from the `math` library

Write a program that imports the `math` library in your program to:

+ print the value of $ \pi $ and $ e $.
+ compute the square $ \sqrt{144} $.
+ compute $ sin(2 \cdot \pi) $

### 024: Using complex numbers

Python supports math operations with complex numbers. Define the complex numbers $ 3 + i $ and $ 100 + 10 i $, with $ i $ being the imaginary part.

Hint: use `j` to represent the imaginary part.

### 025: Generating random numbers

Using the `random` library from Python's standard libary:

+ produce a random integer between 0 and 10 (inclusive).
+ produce a random floating point number between 7.5 and 10.5 (HINT: use `uniform`)

### 026: special functions `bit_length()` and `id()`

Use the `bit_length()` to return the number of bits needed to represent an integer and a floating point number.

Use the `id()` function to get the memory location of those objects.

Redefine the variables used to refer the previous variables and check if the addressed have changed or not.

### 027: hello, lists and unpacking

Create a named collection `months`, containing the name of the months from January to June. Print in the screen the first and 4th month. Using negative indices, get the month before last, and the last month.

Unpack the individual month names in their corresponding variable names.

### 028: hello, list slicing

Create a list with the numbers 1 thru 10 (inclusive).

+ Obtain a sublist of elements from the 2nd to the 5th (inclusive) and print the obtained list. Print also the length of the list using the `len()` function.

+ Obtain the sublist of elements from the 2nd to the one before last. Print the list and its length.

+ Do the same with the sublist of elements from the 2nd to last.

+ Repeat with the sublist of elements from the first to the one before last.

### 029: more unpacking and indexing

Given the following list of strings `["jane", "john", "jill", "jack"]`. Using indexing,

+ Define a variable that gets jack
+ Define another variable that will capture the rest of the names as a list.

### 030: yet more unpacking

Given the following list `[("jane", 21), ("john", 32), ("jill", 45), ("jack", 23)]`. Define a variable that gets jack's name and his associated value in the tuple.

Use the statement `print(f"Hello to {jack!r} who turns {jack_value} today!")` to print the results.

Get the results using negative indexes, and then repeat the exercise using `*_` to ignore the first elements.

### 031: more on using the star `*` expression when unpacking

Consider the following list that contains the scores of a gymnastics event for a player. The scores are sorted in ascending order: `[6.1, 6.5, 6.8, 7.1, 7.3, 7.6, 8.2, 8.9]`.

Calculate:
+ min score
+ max score
+ middles scores (all but the first and last)
+ average score

Use the star operator to implement it.

### 032: accumulating items with `_` while unpacking

Given a task described by the tuple:

```python
task = (1001, "Laundry", "Wash Clothes", "completed")
```

Create a statement that unpacks the first element as `task_id` and the last one as `status`, using the `_` operator to discard the other elements.

### 033: concatenating lists

Create two lists with the numbers 1, 2, 3 and 4, 5, 6. Concatenate them in a new list and print the resulting list.

### 034: Indexing from the back of a list

Create a list with the numbers 1 thru 10 (inclusive). Use negative indices to obtain:

+ the last element from the list
+ the one before last element.
+ the sublist containing the elements from the second to the one before last (included).
+ the sublist containing the last element, the one before last, and the preceding one in that order (HINT: use the slicing syntax with the extra "step" parameter `-1`)

### 035: Creating and accessing list of lists

Create a list with three elements, those elements being themselves lists:
+ 1, 2, 3
+ 4, 5, 6
+ 7, 8, 9

Then print the following elements:
+ third element of the first list
+ first element of the second list
+ second element of the third list

### 036: Iterating over the elements of a list

Create a list with the name of the months from January thru June. Iterate over the elements of the list using `for` printing the results.

### 037: Appending items to a list programmatically

Define an empty list and use a `for` loop to populates that empty list programmatically with the numbers from 0 to 99 using append. Print the list as it is being created.

In the `for` loop using the expression `range(start, end)`.

### 038: Sorting a list of numbers

Use the `sorted()` function to sort a set of 10 random floating point numbers.

### 039: sorting with a custom function

Define a simple class `Person` with `name` and `age` properties. Create a list of several instances of `Person` and sort them by age using `sorted()`.

### 040: Reversing a list of elements with `reverse`/`reversed`

Create a list with the numbers 1 thru 5 (inclusive). Use `reverse` and `reversed` to reverse the list. What is the difference?

### 041: Concatenate the elements of a list into a string using `str.join()`

Use `str.join()` to convert a list of characters, strings and numbers into a single string using `join()`.

+ characters: a, b, c
+ strings: alpha, beta, gamma
+ numbers: 1, 2, 3, 4, 5

Hint 1: Consider using `"".join()`
Hint 2: To convert a list of numbers into a single string you will have to convert each of the numbers. Consider using `map()`.

### 042: Splitting a string to create a list of strings

Given the multiline string:

```
1001,Homework,5
1002,Laundry,3
1003,Grocery,4
```

Use `split` to create a list of lists with the individual items, so that the result is:

```python
[['1001', 'Homework', '5'], ['1002', 'Laundry', '3'], ... ]
```

### 043: split and rsplit

Use `split` and `rsplit` on the multiline string:

```
This is line 1
This is line 2
This is line 3
This is line 4
This is line 5
```

| NOTE: |
| :---- |
| `rsplit()` starts the splitting from the end of the string and works backwards to the front. |
| Both `split()` and `rsplit()` allows for a second parameter `maxsplit`. |

+ Use `split()` to obtain a list with each each line.
+ Use `split()` to obtain a list in which the first three elements are the first three lines, and the fourth element is the remaining string (`"This is line 4\nThis is line5"`)
+ Use `rsplit()` to obtain a list with each line.
+ Use `rsplit()` to obtain a list in which the first element is the first two lines (`"This is line 1\nThis is line 2"`), and the rest are the corresponding lines 3, 4, and 5.


to understand the difference between them. What happens when you use the second argument as `3`.

### 044: Find a first match in a list or iterable

Given a list containing the names "Linda", "Tiffany", "Florina", and "Jovann", use the method `index()` to find the first name whose length is 7.

### 045: Using `in` to check if an item belongs to a list

Given the list `["one", 2, "a", False]`, check whether `"foo"` and `"a"` are items in the list.

### 046: lists are mutable

Illustrate with the following example that lists are mutable. Given the list `["one", 2, "a", False]`.

+ Check that you can modify the second element, making it 14.
+ Check that you can append an element to the list.
+ Check that you can remove the first element

### 047: adding elements to a list

Check the different methods that can be used to add elements to a list:

+ `append()`
+ `extend()`
+ `+=`
+ `+`
+ `insert`

Explain what each of the different methods do and identify the scenarios in which they will be useful.

Then write a program doing:
+ define an empty list named `items`.
+ add an element `"one"` using `append()`.
+ add an element `"two"` after the previous one using `append()`.
+ add the element `"three"` using `extend()`.
+ add the elements `"four"` and `"five"` in a single operation using `extend()`.
+ ass the element `"six"` using `+=`
+ add the elements `"seven"` and `"eight"` and `"nine"` using `+=`.
+ create a list by combining `[1, 2, 3]` and `[4, 5, 6, 7, 8]`.
+ Insert the element `0` as the first element in the previous list.
+ Insert the element `3.5` between `3` and `4` within the list.


### 048: Removing items by value

Define a list with the contents `["one", "two", "three", "two"]`. Use `remove()` to remove the element `two`. Are both elements removed?

### 049: Copying a list using slicing

Using the slicing syntax to copy the contents of a list. Validate that the list has been copied.

### 050: sorting the elements of the list

+ Given the list `[1, 4, 2, 6, 3, 5]` sort it *inline* using the `sort()` method.
+ Given the list `["one", "two", 'a', False]`, try to sort it and see what happens.
+ Use `sorted()` to get the sorted list of `[1, 4, 2, 6, 3, 5]` without affecting the original list.

### 051: Custom sorting

Given the list of strings `["Eloy", "carlos", "Antonio", "ascen", "gloria"]`, sort it using the default comparer, and a custom one that dismisses whether the string is capitalized or not.


## 03: Tuples, Sets, an Dictionaries

### 052: Creating and accessing tuples

Create the following:

+ `tuple_1`: the tuple containing the elements 1 and 2.
+ `tuple_2`: the tuple containing the elements a, b, c, d
+ `tuple_3`: the tuple containing the elements 1, 2, 3, 4, 5 without using parentheses.

The print:
+ the first and second element of `tuple_1`
+ the one before last, and last element of `tuple_2`
+ the tuple consisting of elements 2nd thru 4th of `tuple_3`.

### 053: Creating and accessing sets

Create a set statically of numbers with the numbers from 0 to 5.

### 054: Removing duplicates from a list with sets

Generate a list of 100 random numbers in the range 0-9 (inclusive).

+ Create the sublist of unique numbers.
+ Repeat the exercise but this time, report how many random numbers you need to create to have the numbers 0-9. Execute this process multiple times to get an average of how many randoms are needed.

### 055: Complement, Union, and Intersection operations on sets

Consider the set named *sample space*, denoted as $ S = \{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \}$.

And the events also represented by sets:
  + $ A = \{ 0, 2, 4, 6, 8 \}$,
  + $ B = \{ 1, 3, 5, 7, 9 \}$,
  + $ C = \{ 2, 3, 4, 5 \} $,
  + and $ D = \{ 1, 6, 7 \} $.


Use Python to calculate:

1. $ A \cup C $
2. $ A \cap B $
3. $ C' $
4. $ (C' \cap D) \cup B $
5. $ (S \cap C)' $
6. $ A \cap C \cap D' $

Use both the operation names and the overloaded operators.

### 056: Checking if a set is a superset of other

Given the sets:

```python
set1 = { "Idris", "Jason", "Kenneth"}
set2 = { "Jason" }
```

Check whether `set2` is a superset of `set1`.

HINT: use `issuperset` and the overloaded operator `<`.

### 057: Creating a dictionary with literals

Create a dictionary representing a dog with keys name and age and populate it with values.

Then access the individual values to print a message for the dog.

Try to access a non-existing key (e.g., breed) and see what happens. How can you prevent that error.

### 058: Using `get` and specifying default values

Create a dictionary representing a person with keys name and age. Illustrate how you can access the values using both the syntax `d["key"]` and `d.get("key")`. Explore the `get()`'s second parameter to specify a default value when accessing a non-existent property such as nationality.

### 059: Converting a dictionary into a list

Use `list` to convert a dictionary representing a person with keys name and age. Did you get the expected results?

Try again using the `items()` method on the dictionary. What did you get?

Try with the `keys()` and `values()` methods. What did you get?

Iterate through the dictionary printing:

```
key=<key>, value=<value>
```

### 060: Removing keys from a dictionary using `del`

Create a dictionary representing a person, with keys name and age and city. Use `del` to remove the age property, and print the dictionary.

Investigate the methods `pop()` and `popitem()`. Finally, use `clear()` to clear the dictionary.


### 061: Copying a dictionary

Create a dictionary with keys name of the country and value its corresponding capital.

Create a copy of the dictionary using the `copy()` method.

Then add a new capital to the copy and print both dictionaries. Check that the memory address is different.

### 062: Creating a dictionary with a dictionary generator

You can use the following syntax to create dictionaries dynamically:

```python
{key:value for elem in elems}
```

Use this syntax to create a frequency map for the characters found in a string.
For example, the string `jason isaacs` should produce:

```python
' ': 1, 'j': 1, 'a': 3, 's': 2, 'o': 1, 'n': 1, 'i': 1, 'c': 1
```

### 063: creating a dictionary with two lists

In python, it's fairly common to work with two lists in parallel (e.g., in plotting libraries is common to use a list for x-axis values and another for the y-values). However, it might be useful to work with a dictionary in which the keys are one of the lists, and the value the other one.

Consider the following lists with ids and tasks:

```python
ids = [101, 102, 103]
tasks = ["Laundry", "Homework", "Soccer"]
```

Create a dictionary out of the two lists so that you end up with a dictionary like:

```python
desired_output = {101: "Laundry", 102: "Homework", 103: "Soccer"}
```

Hint: consider using the `zip()` function.

### 064: using `dict.fromkeys()`

The function `dict.fromkeys()` lets you create a dictionary whose keys are given in an iterable passed as an argument.

Use that function to create a dictionary whose keys are status, urgency, and content. What are the values given in the dictionary.

Explore the use of `dict.fromkeys()` second parameter to give the dictionary values a default value.

## 04: Ranges, comprehensions, generators, and zip

### 065: creating and iterating over ranges

Create a range object containing the numbers from 0 to 9, print it, and iterate over it printing only the even numbers.

### 066: Materializing ranges

Create a range of the odd numbers from 5 to 15. Materialize it and print the results.

### 067: Hello, list comprehensions

Create a list containing the first cubes from 0 to 9 using both an imperative approach (i.e., using a loop), and a declarative one using a list comprehension.

### 068: nested loops in list comprehensions

Using list comprehensions, create a list of all the months in 2020-2025, so that the resulting list looks like

```python
[
  "Jan, 2020"
  "Feb, 2020"
  "Mar, 2020"
  ...
  "Dec, 2020"
  "Jan, 2021"
  ...
  "Dec, 2025"

]
```

### 069: more nested list comprehensions

Using list comprehensions create a list of lists with all the months from 2020 to 2025, so that the months for a year are defined in their own *vector*.

That is, the resulting list should look like

```python
[
  ["Jan, 2020", "Feb, 2020", ... "Dec, 2020"],
  ["Jan, 2021", "Feb, 2021", ... "Dec, 2021"],
  ["Jan, 2022", "Feb, 2022", ... "Dec, 2022"],
]
```

### 070: combination of elements using list comprehensions and tuples

Create the combination of elements:

$$
(x, y)  \text{ where }  -1 <= x <= 5 \text{ and } 0 <= y <= 1
$$

### 071: list comprehensions and generators

Using a list comprehension, write a snippet that computes the sum of the squares of the first 1,000,000 integers. Calculate the memory used by the list comprehension using `__sizeof__()` dunder method on the list.

Repeat the exercise using a generator that *yields* the next square every time it is called. Apply `__sizeof__()` on the generator function and compare.

### 072: infinite generators

Create an iterable represented by a function `count()` that returns the integer numbers starting from 0. Print the first three elements. Did you get the results you were expecting to get?

Use the same iterable in a `for` loop to print the elements until 10. Can you explain the results?

### 073: generators and list comprehensions

Using [Exercise 072](#072-infinite-generators) as an inspiration, create a generator `count(start, end)` that produces the numbers from `start` to `end`. Then use a list comprehension to collect those values in a list.

### 074: generator comprehensions (aka generator expressions)

A generator comprehension is a special type of syntax for generators that lets you define generators in a much more compact way.

```python
# generator comprehension
(expr for elem in iterable)
```

Use the generator comprehension syntax and the regular syntaxt to create a generator that produces the squares from zero to 9.

Repeat the exercise to return the squares of the first million integers.

### 075: generator expressions within functions

Confirm that you don't need to use the parenthesis in a generator expression when you are creating the generator expression directly in the invocation of a function by creating a snippet that returns the sum of the firs million integers.

### 076: Fibonacci sequence using a generator

Write a snippet that returns the Fibonacci sequence using a generator.

### 077: hello, zip!

Use the `zip()` function to combine the list of numbers from 1 to 3 and the characters a, b, and c.

### 078: zipping iterables with different number of items

By default, `zip()` stops zipping when the iterable with the fewest number of items is exhausted.

Confirm this fact by zipping the range of numbers from 0 to 3 and the list of letters a, b, c, d.

From Python 3.10, an optional parameter `strict` was added to the function. Check what happens when you try to zip iterables of different size when `strict=True` and when `strict=False`.

### 079: zip_longest()

Illustrate the use of `zip_longest` from `itertools` package to zip the iterables `range(3)` and `range(4)`. What is the result when compared to `zip()`.

## 05: String formatting and templating

### 080: old-school string formatting

Although this syntax is considered legacy, create a function `birthday(name, age)` and returns a formatted string that returns "Hello to {name} who turns {age} tomorrow" using the old school syntax:

```python
str_with_%_placeholders % (var1, var2, ..., varN)
```


### 081: more old-school formatting with `format()`

Another old-school way of format strings used `format()` function.

Create a program that uses `format()` to print the message `"My favorite vector is (2, 5)"` where the vector is a variable.

Create another snippet that returns "Hello to Adri who is turning 17 tomorrow, and his favorite number is 5", with "Adri", 17, and 5 being variables.

### 082: using f"..." (f-strings) templatized strings

Repeat the previous exercise [081](#081-more-old-school-formatting-with-format) using f-strings.

### 083: getting the bytes out of a string with `b"<str>"`

Define the string `b"Hello ABC abc 123"`. Print it and create a loop that iterates over its characters. What do you get?

### 084: applying format specifiers in f-strings

The syntax especification when interpolating in f-strings is as follows:

```python
f"Hello, {expr:[padding_char]{<,^,>}width}
```

where
+ `expr` is the interpolated expression.
+ `padding_char` is the character that will be used for padding (optional, default being space).
+ `<`, `^`, `>` sets the alignment to left, center, or right (respectively).
+ `width` is an integer that sets how long the string will expand (for alignment purposes)

As an exercise, given the following lists:

```python
task_ids = [1, 2, 3, 99999]
task_names = ["Do homework", "Laundry", "Pay bills", "012345678901"]
task_urgencies = [5, 3, 4, 999]
```

Use the correct format specifiers to achieve the following report:

```
task_id  task_name  task_urgency
   1     Homework         5
   2     Laundry          3
...
```

Create a function `print_formatted_records(fmt)` that can receive the format specifier and use use it to test different formats. As an example, what format should be used to get the following output?

```
*****Task ID**********Task Name**********Urgency******
********1************Do homework************5*********
********2**************Laundry**************3*********
********3*************Pay bills*************4*********
******99999**********012345678901**********999********
```

### 085: Formatting numbers

Create program that that prints:
+ 1000000007 as a decimal number with thousand separators.
+ 1.23456 as a decimal number with 2 decimal digits
+ 1.23456 as a decimal number with 4 decimal digits
+ 0.00000000412733 using scientific notation
+ 0.00000000412733 using scientific notation with 2 decimal digits
+ 0.00000000412733 using "general notation"
+ 0.00000000412733 using "general notation" with 2 decimal digits
+ 0.179323 as a percentage
+ 0.179323 as a percentage with 2 decimal digits
+ 12 as a hex value with alpha chars in lowercase
+ 12 as a hex value with alpha chars in uppercase
+ 12 as a binary value

### 086: Escaping curly braces in f-strings

Given a product described by the dictionary:

```python
{"name": "Vacuum", "price": 130.675}
```

Write the output:

```
Vacuum: {130.68}
```

### 087: using special specifiers `=` and `!r`

+ Define the variable `x = 57` and print it with the special identifier `=`
+ Define the variable `"hello"` and print it with the special identifier `=`
+ Define the variable `x = 57` and print it with the special identifier `!r`
+ Define the variable `"hello"` and print it with the special identifier `!r`
+ Define a function and print the result of invoking the function using the special identifier `=`

## 06: Functions

### 088: Invoking functions with named parameters

Create a function `birthday(name, age)` and invoke it passing `age` as the 1st parameter and `name` as the 2nd.

### 089: Hello, `**` operator

The `**` operator (as in `**kwargs`) is used to pass a *keyworded*, variable-length argument list to a function.
As with the `*` operator, it behaves differently in the function declaration than it does when invoking the function in the client code, but it follows the same pattern:
+ When defining a function signature, it identifies a parameter as a variable-length, key-value argument.
+ When invoking a function, it lets you pass a dictionary object to a function requiring explicit key-value arguments (or `**kwargs` type of argument).

Create two functions `birthday(name, age)` and `print_birthday_greet(**kwargs)` that print in the console the name and age properties they receive. Then invoke them passing a dictionary object with keys `name` and `age`.

### 090: Hello, default and optional arguments

Create a function `birthday_greet(name, age)` in which `age` is an optional parameter, and `name` has the default value of `stranger` and invoke it with different sets of arguments.

### 091: Default arguments and `**kwargs`

Create an implementation of `birthday_greet(name, age)` using `**kwargs` where `name` has `"stranger"` as the default value and `age` is optional and invoke it with different sets of arguments.

### 092: Lambdas, unnamed inline functions

The syntax to create lambda functions in Python is:

```python
lambda arg1, arg2, ..., argN: impl
```

Lambdas are only considered Pythonic when they are simple, one-off, one-liners. If you plane to reuse the function is much better to use the `def` keyword and name the function.

Create a lambda function that computes the result of adding three numbers. Use that lambda function as an argument to a `compute(n1, n2, n3, op)` function.

### 093: Immediately applying parameters to a lambda

Create a lambda function that returns the next integer to a one given. Invoke it in the same line of declaration.

### 094: Using lambdas as arguments

Consider the following list of named tuples:

```python
from typing import NamedTuple

class Task(NamedTuple):
  title: str
  description: str
  urgency: int


tasks = [
    Task("Homework", "Physics and math", 5),
    Task("Laundry", "Wash clothes", 3),
    Task("Museum", "Egypt exhibit", 4),
    Task("Toaster", "Clean the toaster", 2),
    Task("Camera", "Export photos", 4),
    Task("Floor", "Mop the floor", 3),
    Task("Internet", "Upgrade plan", 5),
    Task("Utility", "Pay bills", 5)
]
```

Use a lambda to get the list sorted by urgency, in reverse order.

### 095: Lambdas and Pythonic solutions

+ Consider the list of numbers: `[-4, 3, 7, 0, -6]`. Sort them using their absolute value. Can you find a more Pythonic way to implement the solution without using a custom lambda?

+ Consider the following list of tuples representing a student's scores in Math, Science, and Art. Find out what tuple has the highest score (i.e., what's the highest value found in all the values). Try to write the more succinct, more Pythonic solution.

```python
scores = [(93, 95, 94), (92, 95, 96), (94, 97, 91), (95, 97, 99)]
```

### 096: functions as objects

Functions are first-class citizens in Pythons. As such, they can be used as arguments to other functions, kept in data containers such as dicts, and lists, etc.

Define the following dummy functions that return a string identifying themselves: `get_mean(data)`, `get_min(data)`, `get_max(data)`.

Define a dictionary with keys: `mean`, `min`, `max` and with values being the functions recently defined.
Then define a function `process_data(data, action)` that applies the given action to the data.

### 097: map, filter, and reduce

The higher order functions `map` and `filter` are available in Python's core package, while `reduce` is available in `functools` standard library.

Familiarize yourself with those functions by creating three snippets that:
+ Use `map` to create a list of squares given a list of integers.
+ Use `filter` to filter out odd numbers from a given list of integers.
+ Use `reduce` to calculate the sum of a given list of numbers.

Do this functions materialize the results?

### 098: `map` as an iterable

The `map` function creates a map iterator which you can use to transform every element of an iterable.

Consider the list of strings `["1.23", "4.56", "7.89"]`. Create a program that transforms that list of strings into a list of floats.

### 099: Hello, closures

Using closures, implement a function `make_power_fn(power)` that returns a function `fn(base)` that ultimately produces the result `base ** power` when invoked.

Create another function `increment_maker(num)` that returns a function that increments its argument by num.

### 100: Weird function signatures

Python functions can have weird function signatures when using operators such as `/` and `*`. Those are typically used in library functions to expose a better DX to its consumers.

Consider the function with signature `def weird(param1, param2, *, prefix=None, **kwargs)`. Within the function, create the code to announce the values of the parameters received.

Try to do the following invocations, explaining the behavior (note: certain invocations might fail):
+ weird("p1", "p2")
+ weird(param2="p2", param1="p1")
+ weird("p1", "p2", "other")
+ weird("p1", "p2", some="some", other="other", values="params")
+ weird("p1", "p2", prefix="yay", some="some", other="other", values="params")

Then define the function `def normal(param1, param2, prefix=None, **kwargs)` and test the invocations that fail. What do you think is the purpose of `*`.

## 07: OOP

### 101: Basics of Classes

Create a class `Duck` with a method `quack()` that announces itself in the console. Create an instance and invoke the method.

### 102: Constructors

Create a class `Duck` with a constructor that takes a name and color attributes. Then create a `quack()` method that announces itself showing the values of those attributes. Check also how you can access the object instance values from outside the class.

### 103: Rectangle class

Create a `Rectangle` class with the following capabilities:

+ A `Rectangle` object can be instantiated by passing its width and height dimensions. (HINT: Python constructors are named `def __init__(self, param1, param2...)`)

+ A `Rectangle` must feature the following instance methods:
  + `scale`: which returns a new `Rectangle` with its dimensions scaled by the given factor
  + `area`: which returns the area of the rectangle
  + `__eq__`: which checks for equality
  + `__repr__`: which provides the string representation of a rectangle (used in `print`)

### 104: Operator overloading

Python supports operator overloading using special method names such as:
+ `__mul__`: when the class instance comes on the left-hand side
+ `__rmul`: when the class instance comes on the right-hand side

Enhance the `Rectangle` class from [Exercise 103](#103-rectangle-class) to support the following syntax:

+ `Rectangle(2, 3) * 2`, which requires implementing `__mul__`
+ `2 * Rectangle(2, 3)`, which requires implementing `__rmul__`

### 105: Class methods

Python support class/static methods through the `@classmethod` decorator. Also, these methods should be declared as:

```python
@classmethod
  def method(cls, <param1>, ...):
      ...
```

Enhance the `Rectangle` class [Exercise 104](#104-operator-overloading) by defining a method `square(side)` which returns rectangle whose dimensiones are the given side.

### 106: The `__dict__` property

The `__dict__` property, when applied to a class instance returns the instance fields; when applied to a class returns the class methods.

Use this property on the `Rectangle` class from [Exercise 105](#105-class-methods) and in an instance of the class.

### 107: Square class using Inheritance

Python syntax for inheritance is:

```python
ClassName(superClassName):
  ...
```

Create a `Square` class that inherits from the `Rectangle` class used in [Exercise 106](#106-the-__dict__-property).

| HINT: |
| :---- |
| You will need to use `super().__init__(...)` to invoke the constructor of the superclass. |

### 108: Abstract classes

Python supports abstract classes by inheriting from a special class named `ABC`.

Create a simple class hierarchy following thse guidelines:
+ Create an abstract base class `Shape`. (HINT: you will need to `from abc import ABC`)

    + Create an empty implementation for the methods `area` and `scale`. This will set the interface. (HINT: to create empty implementations you can either use `pass` or `...`. Also, use the `@abstractmethod` decorator to tag the method as abstract)

    + Create an implementation of `__eq__` that relies on `__dict__` to check for equality, based on the underlying properties.

    + Create an implementation of `__mul__` and `__rmul__` that rely on `scale()`.

+ Create a concrete class `Rectangle` respecting the behavior implemented in the previous exercises.

+ Create a concrete class `Square` inheriting from `Rectangle` and respecting the behavior implemented in the previous exercises.

+ Create a concrete class `Circle`.

### 109: Static properties

You can create static properties for a class by declaring them outside of any method.

Create a class with a static property `class_name` set to the name of the class, and another property `num_instances` to track the number of instances created.

### 110: Getters and Setters

There are two ways of creating setters and getters in Python.

+ using the `property()` function which identifies the functions that will act as setters, getters, and delete functions (note that you have to include a snippet of *static code* (not bound to any method) in the class definition):

    ```python
    def set_something(self, value):
      self.__something = value

    def get_something(self):
      return self.__something

    def del_something(self):
      del self.__something

    something = property(get_something, set_something, del_something)
    ```

+ using the `@property` decorator on the functions

    ```python
    @property
    def get_something(self):
      return self.__something

    @something.setter
    def set_something(self, value):
      self.__something = value

    @something.deleter
    def del_something(self):
      del self.__something
    ```

Create a simple `Person` class with name and age properties using the two approaches described above.

### 111: Creating read-only and write-only attributes

Banking on the `@property` decorator introduced in [Exercise 110](#110-getters-and-setters) it becomes very easy to create read-only and write-only managed attributes.

Create a `Person` class that includes:
  + a `password` attribute that is a write-only attribute
  + a `name` attribute that is read-only and can only be set in the constructor.

Hint: You will have to define the getter for the password attribute to be able to define the getter. In the implementation of the getter, you should raise an `AttributeError` exception.

### 112: Private fields in Python classes

Python does not support private/public qualifiers for class methods and attributes.

However, it is customary to prefix internal implementation methods and attributes with `_`. That approach gives a visual indication to the reader that those methods and attributes should not be used from consumer code. Note that this does not prevent the client code to use them.

Python also supports prefixing your methods and attributes with a double underscore `__`. This approach forces a *name mangling*, so that it'll be much more difficult for the class consumer to use that method or attribute (yet, it will be possible).

As a result, it is conventional to:
+ Use `_prefix` for names used in internal implementation details, but that you **want** to keep available to subclasses and end-consumer code.

+ Use `__prefix` for names used in internal implementation details that you **don't want** to make available to any code outside of the current class.

Create a class that have both type of fields to illustrate the concepts above. Namely:
+ when using `_prefix` the attribute/method is available to subclasses and consumer code. It is commonly called *protected attribute*.
+ when using `__prefix` the attribute/method is not available to subclasses or consumer code. It is commonly called *private attribute*.

Create a class `Vehicle` with private property `num_wheels` and a *hidden* property `has_engine`. Then define a subclass `Car` and verify that you can access the private property, but not the hidden one.


### 113: Checking the type of a class instance with `isinstance()`

The built-in function `isinstance()` lets you check if a class is of a particular type.

Create a simple class hierarchy (e.g., Vehicle, Car) and instantiate an object of each type.

Use `isinstance` to check:
+ whether it returns `True` when checking the `Vehicle` instance against `Vehicle` class.
+ whether it returns `True` when checking the `Car` instance against `Car` class.
+ whether it returns `True` when checking the `Vehicle` instance against `Car` class.
+ whether it returns `True` when checking the `Car` instance against `Vehicle` class.

What can you derive from the results?

### 114: Using `isinstance()` with built-in types

You can also use `isinstance()` to check for the type of built-in types using:
+ `str` for strings
+ `int` for integers
+ `float` for floating-point numbers
+ `complex` for complex numbers
+ `bool` for booleans
+ `list` for lists
+ `tuple` for tuples
+ `range` for ranges
+ `dict` for dictionaries
+ `set` for sets



Use `isinstance` to check:
+ that a string variable is actually a string
+ that a tuple is actually a tuple
+ that a dictionary is actually a dictionary

### 115: Using `issubclass()` to check if a class is a subclass of another class

The function `issubclass()` lets you check if a class is of a particular type.

| NOTE: |
| :---- |
| `issubclass` requires classes not instances. |

Create a simple class hierarchy (e.g., Vehicle, Car) and validate the behavior of `issubclass`.

How would you use `issubclass` if you only have access to a particular instance and not the class? (HINT: look for extra properties on the instance)

## 08: Working with libraries

### 116: Hello, user-defined library

You can import your own custom modules using the same syntax used for core packages:

```python
from [<dir>.]<lib> import <lib_fn_or_property>
```

Create a library in a source file `my_lib.py` in the same directory as the main program. In it, define a function `greet_me()` that prints a message. Define also a `square()` function that returns the square of a number given. Then import that library in the main program and invoke those functions.

### 117: Importing libraries defined in a folder

Python allows you to reference libraries that sit on subdirectories.

Create a `utils/` folder and define a source file `my_lib.py` and define a function `cube(num)`. Import the function and use it in the main program. Import also the `square()` function from exercise [116: Hello, custom library](#116-hello-custom-library).

HINT: you might need to add an empty `__init__.py` file within the `/utils` folder to make Python recognize the folder as a package.

### 118: The concept of `"main"` in modules

There are Python files that can be used both as libraries (whose individual elements might be imported into a larger program), or executed as standalone scripts.

In those cases you will find the following piece of code useful:

```python
if __name__ == "__main__":
  # ... things to run as standalone script ...
```

Create a module `/utils/db_module.py` that exposes two functions `delete_db()` and `create_db()` that announce themselves using `print()`.

Include a code snippet such as the one above so that when invoking the module as a standalone program using `python ./utils/db_module.py` the main section is executed, but when importing it on another main program, that section is not.

Confirm that when removing the guard `if __name__ == "__main__"` those functions are executed as side-effects when the module is imported.

## 09: Type Hints and DocStrings

### 119: Hello, informal docstring

Create a program with a function `greet_me()` that self announces itself. Document the function using the informal approach of DocStrings as shown below:

```python
"""Summary line for the "Python thingy" being documented.

Details spread across multiple lines describing the Python thingy,
how to use it, recommendations, examples, limitations, etc.
"""
```

In `main()`, invoke the function and check how the IDE displays the information about the function when you hover your mouse over the invocation.

### 120: Hello, function docstring with parameters

Create a program with a function `quotient(dividend, divisor, taking_int=False) -> float` that performs a division or integer division depending on the third parameter. Document the function using the following syntax that includes details about the parameters received and returned values:

```python
"""Summary line describing what the function does.

Args:
  param1 (str): The description for param1,whose type is string.
  param2 (bool, optional): The description for param2, which is an optional boolean

Returns:
  list: a list of strings

Raises:
  ValueError: when the given name is empty
"""
```

### 121: Hello, alt docstring for functions

There's an alternative syntax for documenting functions:

```python
"""Summary line describing what the function does.

:param1: str, The description for param1, whose type is string.
:param2: bool | None, The description for param2, which is an optional boolean

:return list, a list of strings
:raises ValueError, when the given name is empty
"""
```

Create a program with a function `quotient(dividend, divisor, taking_int=False) -> float` that performs a division or integer division depending on the third parameter. Document the function using the following syntax that includes details about the parameters received and returned values.

### 122: Hello, function type hints

Type hints are type annotations that can be added to Python code to indicate the type of variables, parameters, returned values, etc.

Note that Python doesn't enforce types, so you will need to use a separate type checker.

Define a class with a static property and a method `say_hello(s)` that returns a greeting and annotate it.

### 123: Annotating complex types

Complex types might require importing the `typing` package. In most modern Python, instead of `typing` you might import `collections.abc`.

Create a function `my_fun()` that takes a list of `float` and returns a function that takes an int and a boolean and returns a string.

HINT: you must use `Callable` to model arguments that are functions. The syntax is:

```python
from collections.abc import Callable

Callable[[arg1_type, arg2_type, ... , argN_type], ret_type]
```

### 124: Creating types

You can create types that can be then used to annotate types (a sort of alias).

Create a type `NestedList` as a list of lists of strings. Then create a variable `my_super_list` of that type.

### 125: Annotating dicts

Create a dictionary whose keys are strings and whose values are floats and annotate it using type hints.

### 126: Annotating unions

A union lets you specify two different types for a given attributes.

Create a function `load_model()` that takes a model_name (string) and optionally a `cache_folder` that can be a string a `Path` or nothing and returns nothing.

Use both the older syntax `Union[type1, type2]` and the new one `type1 | type2`.

### 127: using `any`

You can use `any` type annotations when nothing else matches, or you want to explicitly state that the function doesn't care about the type it receives or returns.

Create a function `foo()` that returns a single argument `any`.

### 128: using `Optional`

You can use the `Optional` type to declare an argument as optional. In more modern Python, `Optional` is commonly changed for a union of `type | None`.

Create a function `foo()` that takes a single optional boolean argument and returns nothing.

### 129: using `Sequence`

You can use `Sequence[type]` to annotate objects that can be indexed such as lists, tuples, strings, etc.

Create a function `print_sequence_elems(sequence)` that takes a sequence and prints its elements.

Can you use that annotation with a `Set` or `dict`?

### 130: using `tuple`

You can use `tuple[type1, type2, ..., typeN]` to annotate a tuple and its types.

Create a 4-tuple that is used to hold int, int, float, string.

## 10: Files

### 131: building paths with `pathlib`

The `/` is overloaded in pathlib to allow you build paths in a succinct and intuitive way.

Create the file path `/path/to/file.ext` using this operator by creating a path `/path` and then adding the other components.

### 132: renaming files

Create a simple file renaming program that given a path, a prefix pattern, and a wildcard of files, scans that path and copies and renames all the files matching the wildcard using the rule:

```
{prefix_pattern}_{counter}.{original extension}
```

on an output directory.

For example, if you have a directory with the files:

```
orig/diagram.png
orig/IMG_1642.jpg
orig/IMG_4598.jpg
orig/IMG_1763.jpg
orig/README.md
```

and you set `prefix_pattern =  "photo"`, `wildcard = IMG*.jpg`, `orig_path = orig/`, `out_path = out/`

the program should renames the files into:

```
out/photo_001.jpg
out/photo_002.jpg
out/photo_003.jpg
```

by using `photo` as the `out_prefix_pattern`.

HINT: use the `glob()` method to scan a given directory for files matching a pattern. Use `shutil` to copy a file from a directory to another.

## 11: The `with` statement

### 133: using `with` to control file exceptions

The `with` statement is used in exception handling code to simplify the management of resources such as files and database connections, so that they are correctly closed in error situations.

Consider a block of code that opens a file for writing, writes a string into that file, and then closes the file.

Write three different snippets:

1. Don't use any exception control. Explain why the approach is weak.

2. Use try/catch/finally to solve all the problems of the first approach.

3. Use `with` and discuss the functionality and readability of this approach.

### 134: providing support to `with` in custom classes

Write a simple class `MessageWriter` that supports the following syntax:

```python
with MessageWriter("filename") as xfile:
    xfile.write(str)
```

When using the previous approach, `MessageWriter` should write the given string to a file, doing proper resource management with the file.

HINT: To provide support to `with` in a custom class, the class will have to implement the magic methods `__enter__(self)` and `__exit__(self, exception_type, exception_value, traceback)`.

## 12: Interacting with the underlying OS

### 135: exiting a program with `sys.exit()`

Create a program that simulates the rolling of a dice and reports the number of consecutive times you obtain an even number. When an odd number is found the program should finish using `sys.exit()`.

NOTE: the `quit()` is similar to `sys.exit()`, but `sys.exit()` is preferred. For example, `quit()` function does not work well on notebook cells.

### 136: exiting a program by raising a `SystemExit`

You can raise a `SystemExit` exception to terminate a running program, and it is more portable than `quit()` as it works on notebook cells tool.

Create a program that simulates the rolling of a dice and reports the number of consecutive times you obtain an even number. When an odd number is found the program should finish using a `SystemExit`.

## 13: Date and Time

### 137: basics of a datetime object

The `datetime` module contains three primary types of objects:
+ `date`
+ `time`
+ `datetime`

Arithmetic operations for these objects are only supported within the same data type, but it is easy to convert from one to the other.

1. Create a variable that holds today's date.
2. Create a variable that holds current time.
3. Create a variable that holds the first day of 2025.
4. Create a variable that holds noon's time.
5. Create a variable tha holds current datetime.
6. Create a variable that holds the datetime `1974-02-05T14:05:48`
7. Try to subtract noon from today's date. What exception do you get?
8. Convert a date to a datetime using `datetime()`.
9. Combine a date and a time using `datetime.combine()`.

### 138: parsing a string into a timezone-aware datetime object

Python can parse a string representing a datetime into a `datetime` object using `datetime.strptime()`. Use this function to parse:

1. 1974-02-05T14:05:18
2. 17/05/2008 23:15:47

| HINT: |
| :---- |
| You will need to provide the format to `strptime` (see https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat) for examples. |

### 139: constructing timezone-aware datetime objects

A `datetime` object is considered naive if it is unaware of the timezone information.

To make it timezone aware, you have to provide the UTC offset and timezone abbreviation as a function of date and time.

Build a timezone-aware datetime object by:
1. Defining a `datetime` object and passing the `tzinfo` information set to your timezone. You will have to use the `timezone` object before that.

2. Repeat the same exercise giving a name to the `timezone` and use `dt.tzname()` to retrieve it.

### 140: computing time differences

Time differences are computed using the `timedelta` function included in `datetime` package.

Compute:
1. The difference between now and `1974-02-05` (no time).
2. The number of days between those dates.
3. The number of seconds between those dates.
4. Define a function `get_date_n_days_after_today` that returns the date resulting from adding `n` days after today's date.
5. Define a function `get_date_n_days_before_today` that returns the date resulting from subtracting `n` days before today's date.

## 14: More on operators

### 141: falsy values and short-circuiting

You can use `and` and `or` boolean operators to create expressions in Python.

+ `or` can be used in an expression to return the value of the first parameter if it is not *falsy*, and return the second if it is. This can become useful in expressions to obtain a default value.

+ `and` in an expression only evaluates the second argument if the first one is true. As a result you can use `x and y` as a shortcut for `if x if False then x else y`.

Create a snippet that prompts the user for his/her name. Using an `or` expression, assign the value `"stranger"` if no value is provided, and greet the user.

Create another snippet that uses `and` expression between two variables `x` and `y` and check what happens when you assign values such as `True` and `False`, `5` and `0`, `"some"` and `""`.

### 142: is operator

`is` is the identity operator, returning `True` if and only if two objects are the same object.

1. Create two strings with values `"hello"` and `"hello"`. Compare them with `==` and `is`.

2. Create two numbers with values `5` and `5`. Compare them with `==` and `is`.

3. Create a boolean variable `True`. Compare it with `True` using `==` and `is`.

4. Create a simple `Person` class and implement `__eq__`. Create two identical instances of the `Person` class (e.g., `Person("Jason", 53)`) and compare them with `is` and `==`. What is the result if you remove the implementation of `__eq__()`?

5. Create two lists with the items `[1, 2, 3]`. Compare them with `==` and `is`.

### 143: in operator

`in` is the membership operator, returning `True` if a value is contained in a sequence.

1. Create a list and use the `in` operator to check if a given value is in the list.
2. Create a dictionary and use the `in` operator to check if a given key is in the list of keys of the dictionary.

### 144: the ternary operator

The syntax for the ternary operator in Python is:

```python
result_if_true if condition else result_if_false
```

Use the ternary operator to create an expression that returns `True` when passed a number over 18 and wrap it in a function called `is_adult`. Can you use another simpler expression to obtain the same result? Demonstrate you can defining an `is_adult2()` function.

## 15: More on strings

### 145: a bunch of string methods

Strings has a bunch of built-in methods that operate on the same way &mdash; they are applied to an string instance and return either a new immutable string without modifying the original, a boolean (`is*()` methods), an index (`find()`), or a list of strings (`split()`):

| String Method | Description |
|---------------|-------------|
| `isalpha()` | Returns true if the string contains only chars and is not empty |
| `isalnum()` | True if the string contains characters or digits and is not empty |
| `isdecimal()` | True if a string contains digits and is not empty |
| `lower()` | Returns a lowercase version of a string |
| `islower()` | True if a string is lowercase |
| `upper()` | Returns an uppercase version of a string |
| `isupper()` | True if a string is uppercase |
| `title()` | Gets a capitalized version of a string |
| `startswith()` | Checks if a string starts with a specific substring |
| `endswith()` | Checks if a string ends with a specific string |
| `replace()` | Replaces a part of a string |
| `split()` | Splits a string on a specific character |
| `strip()` | Trims whitespace characters from a string |
| `join()` | Joins strings |
| `find()` | Finds the position of a substring |

### 146: `len()` and `in` in strings

The built-in function `len()` and the operator `in` can be used in strings.

+ Built a simple program that calculates the length of a "regular" string and the length of a string that contain emojis different emojis such as 😱 and 🛩️.

+ Built a simple program that illustrate the result of `"son" in "Jason Isaacs"`. Use it with a string with emojis.


### 147: escaping characters within a string

Work out how to output the f-string `""{name}" is an actor"`, that is, the name of the actor must be enclosed in double quotes.

### 148: indexing and slicing

Individual characters or sets of characters within a string can be accessed like elements in a list.

Predict the results of the following operations:

```python
name = "foobar"
name[0]       # f
name[1]       # o
name[-1]      # r
name[-2]      # a
name[0:2]     # fo
name[3:]      # bar
name[:2]      # fo
name[1:-1]    # ooba
```

### 149: using `isalnum()` to check whether strings represent alphanumeric values

Check the behavior of `isalnum()` with the strings `"123@!"` and `"123asdf"`.

### 150: using `isalpha()` to check if a string contains only letters

Check the behavior of `isalpha()` with the string `"Homework"` and `"CS101"`.

### 151: using `isnumeric()` to check if a string contain numbers only

Build a program that prompts your age and computes the year you were born. Use `isnumeric()` to validate the user enters a valid age.

Check the behavior of `isnumeric()` with decimal, numbers in scientific notation, and negative numbers.

### 152: casting strings to numbers

You can use `float("string")` and `int("string")` to cast a string into a floating-point number or an integer. When the casting fails, you'll get a `ValueError`.

Build a program that prompts the user for a number and casts it into a number. Use try-except-else block to handle the exceptions correctly.

### 153: concatenating f-strings into a single string

Given the following dictionary describing font related setting:

```python
settings = {
    "font_size": "large",
    "font": "Arial",
    "color": "Black",
    "align": "center"
}
```

Build the following string using f-strings:

```
font-size=large, font=Arial, color=Black, align=center
```

## 16: More on booleans

###  154: boolean coalescing rules

The `bool` type can have the values `True` and `False`.

There are a few coalescing rules for non-boolean types to be aware of:
+ numbers are always `True` except for number `0`.
+ strings are `False` only when empty.
+ lists, tuples, sets, and dictionaries are `False` only when empty.

You can check if a given variable is bool using `isinstance(var, bool)`.

Create a program illustrating the validation rules explained above.

### 155: `any` and `all`

Python defines the following built-in functions that receive an iterable:
+ `any()` returns `True` if any of the elements of the iterable is `True`.
+ `all()` returns `True` if all of the elements of the iterable are `True`.

Create a simple program that illustrates the behavior of `any` and `all`.

## 17: enums

### 156: Hello, enums

Enums are readable names bound to constant values.

Create an enum `State` with the values `DISABLED`, which should be 0, and `ENABLED` which should be 1.

Then, create a piece of code that refers to the enum using:
+ the defined values (as in `State.ENABLED`).
+ the given value (as in `State(1)`).
+ the defined value using the dictionary syntax (as in `State["ENABLED"]`).

Demonstrate how can you access the value given to the constant using `.value`.
Use `list` to obtain the list of available values, and `len` to obtain the count of the values.

### 157: emulating constants with enums

Python has no language construct to enforce that a variable should have a constant value, but you can emulate a constant with `Enum`.

Create a program that define an `Enum` named `Constants` with two constants `WIDTH` with value 1024 and `HEIGHT` with value 768.

+ Use `print()` to print the value of the constants.
+ Confirm that you cannot change the value assigned to `WIDTH` or `HEIGHT`.
+ How would you rate the DX when compared to the other alternative (using naming conventions such as defining variables in all caps `WIDTH = 1024`).

## 18: Reading user input

### 158: using `input()` and `getpass()`

Define a program which features an internal vault with usernames and passwords. In the program ask the user for their username and password and keeps asking until both are correct, or the max number of attempts is reach (in which case the user should be in locked status).

## 19: More on functions

### 159: by_ref_always

In Python, arguments are always passed by reference, which means that side-effects within the function will be visible outside.

However, some Python objects are immutable, so it will feel that those objects are passed by value instead.

Create a program the changes the value of a number, a string, a tuple, a list, and a custom `Person` class that you create. Within the function, and in the outer scope print the value and the memory.

### 160: returning multiple values

Python can return multiple values by explicitly returning a tuple, or by using the syntax `arg1, arg2, arg3`.

Create a function that returns three arguments and unpack them as individual arguments within the function.

### 161: nested function and `nonlocal`

Python allows functions defined within function. A variable defined in the outer function will be available for reading in the nested function, but to modify a variable defined in the outer function you will have to use the keyword `nonlocal`.

Define a function `count()` which defines a variable count initialized to 0. Define a nested function increment which increments the value of `count` when invoked. Return this function and use it in `main()`.

### 162: more on `*` in functions

Python allows you to define functions with default arguments, so that if the client does not provide it, it will take the default value.

For example, you can do:

```python
numbers.sort() # using default args
numbers.sort(reverse=True) # passing an argument
```

It's common for this functions to use signatures such as:

```python
sort(*, key=None, reverse=False)
```

The `*` in the method signature dictates that all the arguments following the asterisk should be named, that is, cannot be positional as in `sort(False)`.

1. Define a list of numbers and use the `sort()` method with and without parameters. Confirm that you cannot use positional arguments.

2. Create a `Task` class with a constructor that takes the title, description, and urgency of the task. Define `complete_task()` method in the program (outside the class), that takes the task to complete and a note with a default value `""`. Use the `*` to force that the note should not be sent as positional. This function should set the task status to `"completed", and add a note to the task. Create a task, complete it, and print its contents including the note.


| NOTE: |
| :---- |
| When we define functions, we refer to the variables specified in the function head as *parameters*. When we call functions, we refer to the variables we use as arguments.

> Parameters are the variables used in a function definition; arguments are the variables used in a function's invocation. |


### 163: gotchas when setting default arguments for mutable types

Create a Task class with the fields title, description, and urgency. Then define a standalone function `complete_task()` that accepts the task to complete, and a `group` argument. Give the default value `[]` to this group, with the intention of creating an empty list when none is given.

Within the function, set the task status to completed, add the task title to the group, and return the group.

Then, in the `main()` function, create three tasks `Homework`, `Videogames`, `Watch Movies`. Create a list called `boring_tasks` initialized to the empty list.
Then invoke `complete_task()` for `Homework` passing the `boring_tasks` list. Print the result of completing the task (which should be the group with the task title added to `boring_tasks`).

Then invoke `complete_task()` for `Videogames` without passing a list. Print the result of completing the task. What is the result?

Invoke again `complete_task()` for `Watch Movies` without passing a list. Print the result of completing the task. What is the result?

HINT: use `id()` to check the memory addresses of the results and try to explain why this happens.

How would you fix it? What is the recommendation when you want to have this behavior for mutable types? Rewrite the program to make it work differently.


### 164: partial functions

We often define multiple parameters in a function so that it can handle different forms of input to derive the needed result for different scenarios.

Define a function `run_stats_model(dataset, model, output_path)` that return certain calculated statistics.

The function accepts three arguments to make it sufficiently generic:

```python
run_stats_model(dataset_a1, "model_a", "project_a/stats/")
run_stats_model(dataset_a2, "model_a", "project_a/stats/")
run_stats_model(dataset_b1, "model_b", "project_b/stats/")
run_stats_model(dataset_b2, "model_b", "project_b/stats/")
```

However, this makes the function quite verbose and complicates the DX.

A poor man's solution is defining a function such as:

```python
def run_stats_model_a(dataset):
  results = run_stats_model(dataset, "model_a", "project_a/stats")
  return results
```

However, there's a more pythonic way using the `partial()` function from `functools`.

Use both approaches in an example.

### 165: putting a default value where there isn't one

`partial` can be very useful when you need to set a default value on a function where there isn't one.

Using `partial`, define a function `square` which wraps the power function `pow`. Test the results.


### 166: cache and memoization using `functools`

The `@cache` decorator from `functools` lets you implement memoization very easily.

Define a function that returns the fibonacci sequence for given number (e.g., `fibonacci(n)`). Using perf counters, calculate the time it takes to generate the first 40 fibonacci numbers.

Reimplement the function, this time using the `@cache` anotation from `functools`. What is the time difference.

### 167: function overloading with `@singledispatch`

While Python doesn't allow function overloading, the `@singledispatch` decorator from `functools` allow to define a set of functions (variants in Python parlance) for one main function to handle different types of arguments.

Define an overloaded function `process(data)` that:
+ prints the data if the argument passed is str, int, or list
+ announces the type of data received otherwise

### 168: using `*_` in functions

In Python, you use `*_` in a function definition to ignore positional parameters. It is typically used when a function needs to conform with certain specification, but you don't intend to use the arguments passed in the function implementation.

Create a function `foo(*_)` and invoke it without arguments, with one positional argument, and with several positional arguments. Try to invoke the function with keyword argument.

### 169: using `...`

The `Ellipsis` object (or `...`) is a built-in constant that is useful in many different circumstances:

It can be used in function definitions as a placeholder (empty implementation):

```python
def fn_stub():
    ... # will implement later
```

In type hints, it can be used to announce that the object can contain an arbitrary number of elements:

```python
numbers: tuple[int, ...]
```

It can also be used to make the function specification more flexible, as in:

```python
def fn(a: int, b: int, sum: Callable[..., int])
```

1. Define a function `fn_stub` and use ellipsis to give it an empty implementation. Does it compile?

2. Define a tuple that can contain a variable number of ints. Confirm that it lets you create a tuple with 0, 1, 2, numbers, but that you cannot store a string on the tuple.

3. Define the function `def fn(a: int, b: int, sum: Callable[..., int])` and invoke it. What is the first parameter passed to sum?

### 20: More on loops

### 170: range in loops

Create a range that gives you the numbers from 0 to 100 (excluded) in steps of 10. Use a loop to print the results.

### 171: enumerate in loops

Create a range to return the numbers from 50 to 55 (excluded). Use a loop that prints:
```
0: 50
1: 51
2: 52
3: 53
4: 54
```

### 172: break and continue

The statements `break` and `continue` work as in other programming languages:

+ `break` &mdash; steps out of the current loop
+ `continue` &mdash; stops current iteration in the loop and goes to the next one

Given the list `[1, 2, 3, 4, 5]`, create a loop that:
+ if the item is divisible by 3, skips to the next iteration
+ if the item is 4, breaks out of the loop
+ otherwise prints the number that is being processed

## 20: Variable scope rule in Python

### 173: global variables

When you declare a variable outside of any function in Python, the variable will be visible to any code after the declaration.

This is called a global variable.

A global variable in Python will be visible without requiring any additional keyword, but you won't be able to modify the variable value directly in any of the functions of your code.
If you want to modify the variable of a global variable within the scope of a function, you need to use the `global` keyword as a sort of *variable declaration* within your function.

When you define a variable with the same name as a global name within a function, this new variable will hide the global variable (shadow).

Create a program that defines a global variable `name`.

1. Read the global variable value outside of any function.
2. Change the global variable value outside of any function.
3. Read the global variable value within the `main()` function.
4. Try to change the value of the global variable within the `main()` function.
5. Define a function `update_global()` that updates the value of the global variable using the `global` keyword. Invoke the function from `main()` and check that it works as expected.

### 174: nonlocal

Similarly to the `global` keyword, the `nonlocal` keyword can be used to modify the value of a variable in scope, but that was defined in a different (outer) scope.

Define a function `say_hello()` that:
1. Defines a variable `name` and assigns it the value "Charlize".
2. Defines an inner function `update_name()` that changes the value of `name` by suffixing it with " Theron" and returns the modified `name`.
3. Invokes `prepare_message()` and prints what the function returns.

Invoke the `say_hello()` function from `main()`.

## 21: Decorators

### 175: Hello, decorators

Decorators are a way to change, enhance, and alter the way a function or a method works.

They are defined with the symbol `@`, followed by the decorator name. It should be used right before the function/method definition it is applied to, as in:

```python
@logtime
def greet_me():
    print("Hello to you!")
```

Behind the scenes, a decorator is a plain function that:
1. Takes another function as argument and returns a function
2. Typically, the returned function is an inner function that performs the job associated to the decorator and invokes the passed function when appropriate.

For example:

```python
def logtime(func):
    def wrapper():
        # ... pre-decorator logic here ...
        ret_val = func()
        # ... post-decorator logic here ...
        return ret_val
    return wrapper
```

As a basic example, create a decorator `@announce` that logs in the terminal that the function/method it is applied to has been called.

HINT: use the dunder method `__name__` to get the function name.

Define a simple function `say_hello()`, decorate it with `@announce` and check that it works as expected.

Then define a function `greet(name: str)` and try to use the `@announce` decorator on it. What error do you get?

### 176: hello decorators for functions with parameters

Decorators can also be applied to functions that accepts parameters. The Python runtime will do the necessary to supply the wrapper function of a decorator with the `*args` and `**kwargs` used when invoking the function, so that you can use it in the wrapper as needed.

That is:

```python
def logtime(func):
    def wrapper(*args, **kwargs):
        # ... pre-decorator logic here ...
        ret_val = func(*args, **kwargs)
        # ... post-decorator logic here ...
        return ret_val
    return wrapper
```

As a basic example, create a decorator `@announce` that logs in the terminal that the function/method it is applied to has been called.

HINT: use the dunder method `__name__` to get the function name.

Define a simple function `say_hello()`, decorate it with `@announce` and check that it works as expected.

Then define a function `greet(name: str)` and try to use the `@announce` decorator on it and check that it works.

Finally, define a function `get_greeting(name: str, age: int)` and check that you can also use the decorator `@announce` on it.


| NOTE (arguments vs. parameters): |
| :---- |
| In Python, parameters are the placeholders defined in the function definition. Arguments are the actual values passed when invoking the function. |


### 177: Checking a function's execution time with a decorator

Define a decorator `@logtime` the tracks and displays the execution time it is applied to.

HINTS:
+ use `time.perf_counter()` to calculate the time a function has taken.
+ define the inner function as receiving `*args` and `**kwargs` and make sure you invoke the function with those.

Then define a program with a couple of functions:
+ `run_with_random_delay()`, which simulates a workload by calculating a random delay between 1 and 5 and then invoking `time.sleep()` with that value. The function must return the delay.
+ `run_with_delay(min_wait, max_wait, *, label: str=None, verbose=False)`, which simulates a workload by calculating a random delay between min_wait and max_wait, and optionally printing the label and some additional details if verbose is True.

Test the program execution to understand how `*args` and `**kwargs` are being passed to the inner function of the decorator.

### 178: a generic monitor decorator

Create a decorator `@monitor` which announces the function it is applied to.
That is:
+ Should print: ">>> <function name> invoked", before the function has been executed
+ Should print: ">>> <function name> complete", after the function has been executed
+ Should return the value of executing the function it has been applied to

Validate the `@monitor` can be used for functions that receive no parameters, and functions that receive all kind of parameters.

Test it with:
+ `run_with_random_delay()`, which simulates a workload by calculating a random delay between 1 and 5 and then invoking `time.sleep()` with that value. The function must return the delay.
+ `run_with_delay(min_wait, max_wait, *, label: str=None, verbose=False)`, which simulates a workload by calculating a random delay between min_wait and max_wait, and optionally printing the label and some additional details if verbose is True.

### 179: decorator with arguments

Because the decorator signature is fixed:
+ receives the function is applied to
+ returns the function it has to be executed instead of the function it is applied to.

You need to use a workaround to define a decorator that accepts arguments. This workaround consists of wrapping the decorator into another function that accepts an argument.

It's better visualized using code:

```python
def decorator_with_args(arg1, arg2, arg3):
    def regular_decorator(func):
        def wrapper(*args, **kwargs):
            # ... pre-decorator logic here using arg1, arg2, arg3...
            ret_val = func(*args, **kwargs) # can use arg1, arg2, arg3 in invocation too
            # ... post-decorator logic here using arg1, arg2, arg3...

        return wrapper
    return regular_decorator

@decorator_with_args(val1, val2, val3)
def fn():
    # ... function implementation ...
```

Create a `@monitor(label: str | None)` decorator that allows for passing an optional label.

### 180: Preserving the decorated function's metadata in an parameter-less decorator

When decorating a function, it's docstring (and other metadata) will be lost:

Define a naive decorator `@monitor` that announces the function it has been applied to. Then define two functions `say_hi()` and `say_hello()` and decorate the latter with `@monitor`. Then print in the console the properties `__doc__` and `__name__` of both functions.

Define a 2nd version of `@monitor` that uses `@functools.wraps(func)` in the wrapper function (the one that actually invokes the function).

### 181: Preserving the decorated function's metadata in a decorator with parameters

Create a decorator `@monitor(msg)` that announces the function it has been applied and accepts as argument a custom label that will be used when supplied.

Make sure that you use `@functools.wraps(func)` to ensure that the function's metadata is not lost.

## 22: Introspection/Reflection

### 182: hello, type

You can use `type()` to get the type of an object.

Create a program that defines a simple class `Person`. Define in the program an integer variable, a string variable, and a tuple and apply `type()` to each of them printing the results.

### 183: hello, dir

The `dir()` global function provides all the methods and attributes of an object.
Define a string variable and print the result of using `dir()` on that variable.

## 23: More on exceptions

### 184: try-except block

A somewhat complete form of a try-except block looks like the following:

```python
try:
    # block of code that might raise exception
except ExceptionType_1 [as exc1]:
    # ExceptionType_1 error handler,
    # optionally using exc1 as var containing the exception
except ExceptionType_2 [as exc2]:
    # ExceptionType_2 error handler,
    # optionally using exc2 as var containing the exception
...
except ExceptionType_N [as excN]:
    # ExceptionType_N error handler,
    # optionally using excN as var containing the exception
else:
    # code to run if no exception raised
finally:
    # code to run no matter whether exception raised or not
```

Create a `divide(dividend, divisor)` function that correctly deals with:
+ arguments passed not being numbers
+ divisor is zero

Make sure that you implement logic in the `else` and `finally` sections.

### 185: hello, raise

Exceptions are thrown using the `raise` statement.

```python
raise Exc_Type("reason")
```

Create a simple program that:
+ raises a generic `Exception` exception with the reason "A general exception has been raised" and catch it immediately after, printing the contents of the exception.
+ raises a generic `TypeError` exception with the reason "It was the wrong type" and catch it immediately after, printing the contents of the exception. Use `Exception` as the type you use to catch it. Is there a way to get the type of the exception in the except block? (HINT: try using `type()`)

### 186: hello, custom exceptions

You can easily create your own exception classes by extending the `Exception` class.

Create a custom exception `MyCustomError` (it is customary to suffix the custom exceptions with *Error*). Confirm that you can raise a exception of this type using a reason and check that you can catch it using a `Exception`.

### 187: handling multiple exceptions in a single except clause

You can create a except block that handles different types of exceptions using the syntax:

```python
except (Exc_Type1, Exc_Type2):
    ...
```

Create a function `process_task(text)` that receives a string as argument. The string contains a title and an urgency separated by comma, as in:

```
Do homework,1
```

In the implementation, split the string by comma to get the title and urgency of the task. Then, convert the urgency to an int and then assign the title and urgency as attributes to a `pending_task` variable of type string that you will return (this will fail!).

Create a except block that catches both `AttributeError` and `NameError`. Confirm that the except block catches both types of errors by sending both a non numeric urgency, and a numeric one (so that it fails with `AttributeError`).

### 188: custom messages in built-in exceptions

Exceptions allow you to pass custom messages to built-in exceptions such as `ValueError`.

Create a `NamedTuple` class named `Task` with fields title and urgency:

```python
from typing import NamedTuple

class Task(NamedTuple):
  title: str
  urgency: int
```

Then create a `process_task_str()` function that takes a string containing the title and urgency separated by commas as in:

```
Do homework,1
```

In that function you should:

+ Get the title and urgency from the string by splitting by comma.
+ Try to convert the urgency to an int. If the conversion fails, you should raise a `ValueError` with the custom message `f"Incorrect value for urgency: {urgency_str!r}"`
+ If the conversion works correctly, the corresponding task should be created and returned.

Then, in your main program try invoke that function a task with the data `"Laundry,#3"` in a try-block catching the `ValueError` exception and printing the exception using `print(f"{e}")`, `print(e)`, `print(type(e))`, and `print(type(e).__name__)`.

### 189: exceptions hierarchy and reusing existing exception classes

The following diagram details the most common exceptions in Python:

![Exception hierarchy](pics/exceptions-hierarchy.png)

As a rule of thumb, you shouldn't inherit from `BaseException` to avoid catching system-exiting exceptions such as `SystemExit` or `KeyboardInterrupt`.

Instead, when creating your custom exceptions, you should inherit from `Exception`.

It is also recommended to use the existing class hierarchy instead of creating your own custom classes, as the former will be familiar to Python developers. If necessary, you can supply your own custom message for clarity.

Create a simple `Task` class that can be initialized with a title argument. Within the initializer, check that the type of the argument is a string, and if it's not, raise a `TypeError` exception with a custom message `"Please instantiate Task providing a string as its title"`.

Then in the main program, try to instantiate a `Task` with a title of a different type and in the except block print the exception to confirm the error can be clearly identified.

### 190: custom exception hierarchy

When creating custom exceptions, it is recommended to start simple with a custom base class that does nothing such as:

```python
class MyCustomError(Exception):
    pass
```

And then, create a custom hierarchy from it by inheriting from that one, in which we add additional functionality such as initializers, `__str__` methods, etc.

Create a custom base class `MyCustomError` and a `MyFileExtensionError` that inherits from it. In the implementation of the subclassed exception include an initializer that receives a filepath. In the implementation of the initializer invoke the initializer of the superclass, and set an attribute of `MyFileExtensionError` to the received argument.

Define also a `__str__` method that reports the message `f"The file {self.filepath!r} is not a valid CSV file"`.

In the main program, raise a `MyFileExtensionError` passing the path `"log.txt"` within a try block and print the caught exception and its type. Confirm that you get the expected exception description.

### 191: more on operator overloading

Python allows you to implement operator overloading by simply overloading the following methods in your custom class:

+ `__eq__()` for `==` (equality)
+ `__ne__()` for `!=` (inequality)
+ `__lt__()` for `<` (less than comparisons)
+ `__le__()` for `<=` (less than or equal comparisons)
+ `__gt__()` for `>` (greater than comparisons)
+ `__ge__()` for `>=` (greater than or equal comparisons)
+ `__add__()` for `+` (addition)
+ `__sub__()` for `-` (subtraction)
+ `__mul__()` for `*` (multiplication, class instance on the left-hand side)
+ `__rmul__()` for `*` (multiplication, class instance on the right-hand side)
+ `__truediv__()` for `==` (division)
+ `__floordiv__()` for `//` (integer division)
+ `__mod__()` for `%` (modulus)
+ `__rshift_()` for `>>` (right shift)
+ `__lshift__()` for `<<` (left shift)
+ `__and__()` for `&` (binary and)
+ `__or__()` for `|` (binary or)
+ `__xor__()` for `^` (binary xor)

Create an `Amount` class that accepts an amount and a currency to construct it. Use operator overloading to allow comparing two instances of the amount class with the `>` operator and test it in the main function.

You can use a naive implementation, assuming you can only compare instances of Amount when the currency is the same.

### 191: hello, collection functions

Python provides a group of global functions for collections:

+ `sum` &mdash; returns the sum of the elements of a collection
+ `min` / `max` &mdash; returns the min/max element of a collection
+ `sorted` &mdash; returns a sorted collection from a given one, without mutating the original one.
+ `reversed` &mdash; returns the reversed collection from a given one, without mutating the original one.

Create a collection of 10 random integers, print it, and apply the functions above printing the results.

HINT: you might need to use `list()` to materialize the results when those are lazily-evaluated.

### 192: hello, CLI args

Create a simple CLI program that can be invoked as:

```bash
python my-script.py arg1 arg2 arg3
```

In the script implementation, confirm that you've received three arguments and print the values received.

### 193: CLI tools with argparse

Create a CLI script that returns a greeting and relies on `argparse` with the following functionality:

+ when invoked without parameters or with `--help`/`-h` returns `"This script returns a greeting"`.
+ it has a required argument `-n`/`--name` which is the person's name to greet. The value of the argument should be bound to the `name` variable in your script.
+ it has an optional argument `-t`/`--type` which selects the type of greeting to use between `"formal"`, `"informal"`, and `"friendly"`. It should be bound to a `type` variable.

In the implementation, the script should check the type of greeting to use (if any, otherwise the friendly greeting should be used as the default value for the type), and then print it.

### 194: hello, re module

Python's `re` module provides all the features related to regular expressions. The module supports two *invocation flavors*: OOP and the functional approach.

When using the OOP approach, you first create a `Pattern` object by compiling a string pattern describing the regular expression to use. Then, you use the pattern object to search occurrences that match the pattern, split a string by the pattern, etc.

When using the functional style call, you directly pass the regular expression and the string in the same invocation.

OOP is more verbose, but it's more appropriate when you reuse the same `Pattern` object multiple times, as the compilation can be cached.

Create a program that illustrates how to use the OOP and functional style call for the `re` module by:
1. OOP
  1. Create a pattern by invoking `re.compile()` passing the string `"do"` as the regex string.
  2. Print the contents of the resulting `Pattern` and its type (HINT: use `type().__name__`).
  3. Apply the call `search("do homework")` on the pattern printing the results.
  4. Apply the call `findall("don't do that")` printing the results.
2. Functional
  1. Apply the call `re.search(regex_str, str)` to mimic 1.3 behavior printing the results.
  2. Apply the call `re.findall(regex_str, str)` to mimic 1.4 behavior printing the results.


### 195: hello splitting messy data with regex

Given the string `"field1,field2;field3;field4_field5"`, use the `re` package to split the different fields by following these instructions:

1. Create a regex pattern by invoking `re.compile(<regex_pattern>)`. HINT: use a raw string `r"..."` to specify the pattern.
2. Invoke the `split()` method on the pattern.
3. Print the results.

### 196: hello, raw strings for regex patterns

To create regex patterns, we often need to use raw strings as in `r"pattern"`.

This is needed because the way in which you identify digits (`\d`) or words (`\w`) clashes with Python's syntax for escaping characters in regular strings (e.g., `\t` for tabs, `\n` for newline characters, `\\` for backslash).

If using regular strings, specifying regex patterns becomes even more difficult to read. However, when using raw strings there's no need to escape the backslash characters, thus simplifying their specification.

Create a program that illustrates what is the text that you need to use in a regex expression string to search for matches of `\task` in a text string.

### 197: hello, regex boundary anchors

The boundary anchors let you specify whether a string begins or ends with a particular string pattern:

| Regex | Construct | Description |
| :---- | :-------- | :---------- |
| ^foo | Boundary anchor | Starts with "foo" |
| bar$ | Boundary anchors | Ends with "bar" |
| ^foo bar$ | Boundary anchors | Starts and ends with "foo bar" |

Create a program that uses `re`'s functional style call `search` on the following regex patterns and text strings:

1. Search for "^hi" in "hi, Python!"
2. Search for "task$" in "do the task"
3. Search for "^hi task$" in "hi task"
4. Search for "^hi task$" in "hi Python task"

### 198: hello, regex Quantifiers

Quantifiers are used when you need to search for a pattern appearing a certain number of times:

| Regex | Construct | Description |
| :---- | :-------- | :---------- |
| hi? | Quantifiers | "h" followed by zero or one "i" |
| hi* | Quantifiers | "h" followed by zero or more "i" |
| hi+ | Quantifiers | "h" followed by one or more "i" |
| hi{3} | Quantifiers | "h" followed by three "i" (i.e., "iii") |
| hi{1,3} | Quantifiers | "h" followed by one, two, or three "i" (i.e., "i", "ii", or "iii") |
| hi{2,} | Quantifiers | "h" followed by 2 or more "i" (i.e., "ii", "iii", "iiii", ...) |
| ^foo | Boundary anchor | Starts with "foo" |
| bar$ | Boundary anchors | Ends with "bar" |
| ^foo bar$ | Boundary anchors | Starts and ends with "foo bar" |

The metacharacters `?`, `*`, and `+` are *greedy*, meaning that the regex engine will try to match the longest sequence whenever possible. It is possible to disable the greedy behavior by adding the metacharacter `?` to the quantifier (e.g., `hi+?` for "h" followed by "i" one or more times disabling the greedy behavior).

Given the test string: "h hi hii hiii hiiii"
use the functional style version of `findall` to check the outcome of using the function against the following regex patterns: "hi?", "hi*", "hi+", "hi{3}", "hi{2,3}", "hi{2,}", "hi??", "hi*?", "hi+?", "hi{2,}?"

Print a report by creating a for loop that applies `findall` for each regex pattern in the following format:

```
<regex_pattern_1> ==> <result of invoking findall>
<regex_pattern_2> ==> <result of invoking findall>
...
<regex_pattern_n> ==> <result of invoking findall>
```

Note that the arrow should be aligned in all the invocations.

### 199: hello, regex character classes and sets

The following table lists the most common character sets supported in Python. Note that the table is not exhaustive (i.e., there are more):

| Regex | Construct | Description |
| :---- | :-------- | :---------- |
| \d | character set | any decimal digit |
| \D | character set | any character that is not a decimal digit |
| \s | character set | any whitespace character including space, \t, \n, \r, \f, \v |
| \S | character set | any character that isn't a whitespace |
| \w | character set | any word character (alphanumeric plus underscore) |
| \W | character set | any character that is not a word character |
| . | character set | any character except for newline |
| [abc] | character set | any of "a", "b", or "c" |
| [a-z] | character set | any character in the range "a" to "z" |
| [a-zA-Z0-9] | character set | any character in the ranges "a" to "z", "A" to "Z", or "0" to "9" |
| ^foo | Boundary anchor | Starts with "foo" |
| bar$ | Boundary anchors | Ends with "bar" |
| ^foo bar$ | Boundary anchors | Starts and ends with "foo bar" |
| hi? | Quantifiers | "h" followed by zero or one "i" |
| hi* | Quantifiers | "h" followed by zero or more "i" |
| hi+ | Quantifiers | "h" followed by one or more "i" |
| hi{3} | Quantifiers | "h" followed by three "i" (i.e., "iii") |
| hi{1,3} | Quantifiers | "h" followed by one, two, or three "i" (i.e., "i", "ii", or "iii") |
| hi{2,} | Quantifiers | "h" followed by 2 or more "i" (i.e., "ii", "iii", "iiii", ...) |

Given the test string: "#1$wm_ M\t"
use the functional style version of `findall` to check the outcome of using the function against the following regex patterns: "\d", "\D", "\s", "\S", "\w", "\W", ".", "[lmn]"

Print a report by creating a for loop that applies `findall` for each regex pattern in the following format:

```
<regex_pattern_1> ==> <result of invoking findall>
<regex_pattern_2> ==> <result of invoking findall>
...
<regex_pattern_n> ==> <result of invoking findall>
```

Note that the arrow should be aligned in all the invocations.

### 200: hello, logical operators

The following table lists the logical operators:

| Regex | Construct | Description |
| :---- | :-------- | :---------- |
| a \| b | logical operation | "a" or "b" |
| (abc) | logical operation | "abc" as a group |
| [^a] | logical operation | any character other than "a" |
| ^foo | Boundary anchor | Starts with "foo" |
| bar$ | Boundary anchors | Ends with "bar" |
| ^foo bar$ | Boundary anchors | Starts and ends with "foo bar" |
| \d | character set | any decimal digit |
| \D | character set | any character that is not a decimal digit |
| \s | character set | any whitespace character including space, \t, \n, \r, \f, \v |
| \S | character set | any character that isn't a whitespace |
| \w | character set | any word character (alphanumeric plus underscore) |
| \W | character set | any character that is not a word character |
| . | character set | any character except for newline |
| [abc] | character set | any of "a", "b", or "c" |
| [a-z] | character set | any character in the range "a" to "z" |
| [a-zA-Z0-9] | character set | any character in the ranges "a" to "z", "A" to "Z", or "0" to "9" |
| hi? | Quantifiers | "h" followed by zero or one "i" |
| hi* | Quantifiers | "h" followed by zero or more "i" |
| hi+ | Quantifiers | "h" followed by one or more "i" |
| hi{3} | Quantifiers | "h" followed by three "i" (i.e., "iii") |
| hi{1,3} | Quantifiers | "h" followed by one, two, or three "i" (i.e., "i", "ii", or "iii") |
| hi{2,} | Quantifiers | "h" followed by 2 or more "i" (i.e., "ii", "iii", "iiii", ...) |

Create a program that uses the functional style `findall` to test:

1. The pattern "a|b" with the test string "a c d d b ab"
2. The pattern "a|b" with the test string "c d d b"
3. The pattern "(abc)" with the test string "ab bc abc ac"
4. The pattern "[^a]" with the test string "abcde"

### 201: hello, match objects

To understand the `Match` object we need to introduce the `match()` and `search()` methods  used for pattern searching:
+ `match()` is useful for finding the pattern at the beginning of a string
+ `search()` scans the string from the beginning of the string until it finds a match (if any)

Both methods return a `Match` object, which evaluates to True if a match is identified in the string:

```python
match = re.match("pattern", "string to match") # search can be used as well
if match:
    # ... logic if match found ...
else:
    print("No matches found")
```

A `Match` instance can have multiple groups, which can be obtained using:
+ `match.groups()` &mdash; return a tuple with all the groups matched
+ `match.group()` &mdash; return the entire match object (identical to `match.group(0)`)
+ `match.group(0)` &mdash; return the entire match object
+ `match.group(1)` &mdash; return the first element from the match
+ `match.group(2)` &mdash; return the second element from the match

A `Match` instance, and the corresponding groups also feature a span object with information about the starting and end index of the corresponding match and group. You can access the spans with the `span(n)` method:
+ `span()` &mdash; return the span for the entire match object (identical to `match.span(0)`)
+ `span(0)` &mdash; return the span for the entire match object
+ `span(1)` &mdash; return the span for the first element from the match
+ `span(2)` &mdash; return the span for the second element from the match

The `Span` instance exposes the methods `start()` and `end()` that return the index of the first and last element of the match.


1. Create a snippet that searches for the group of a word character followed by a digit occurring one or more times in the string "xyza2b1c3dd". Try to anticipate the results of the match and then confirm using `match.groups()`, `match.group(n)`, `match.spans()`, `match.group()`, `match.span()`. Then print the start and end of the matched string.

2. Given the string "Homework, urgent; today", which identifies a task name, its priority, and the due date, create the regex pattern that matches the task name and priority as different groups. Then use `groups()`, `group()`, `group(0)`, `group(1)`, and `group(2)` to understand the result of invoking those methods. Try to anticipate the results.

3. Repeat the exercise above with `spans()`, `span()`, `span(0)`, `span(1)`, and `span(2)`.

### 202: hello, search

`search()` returns a `Match` if a match is found anywhere in the string.

1. Given the string "ab12xy34st4ou" invoke search to match one or more several consecutive digits. Try to anticipate the results.
2. Given the string "abxy" invoke search to match one or more several consecutive digits. Try to anticipate the results.

### 203: hello, match

`match()` returns a `Match` only if a match is found at the beginning of the string.

1. Given the string "ab12xy" use `match()` to find one or more consecutive digits. Try to anticipate the results.
2. Given the string "12abxy" use `match()` to find one or more consecutive digits. Try to anticipate the results.

### 204: hello, findall

`findall()` returns a list of strings that match the pattern. When the given regex pattern has multiple groups, the item returned is a tuple.

Note that `findall()` has a particular way of capturing groups. `findall()` returns only the captured groups and not the full match.

1. Given the string "hi hey hello", use `findall()` to match the following sequence of characters:
  1. h
  2. followed by i or e, Don't use groups!
  3. followed by any word character

1. Given the string "Hey hello", use `findall()` to match the following:
  1. h or H, as a group
  2. followed by i or e, as a second group

### 205: hello, finditer

`finditer()` returns an iterator that yields `Match` objects.

Given the string "hi Hey Hello", use `finditer()` to match the following sequence of characters:
  1. h or H, as a group
  2. i or e, as a second group

Use the iterator to understand the results.

### 206: hello, split

`split()` splits a string by the given regex pattern.

Given the string "a1b2c3d4e", use `split()` to split it by the sequence of one or more digits and print the results.

### 207: hello, sub

`sub()` creates a string by replacing the matched string with the given replacement.

Given the string "123,456_789", use `sub()` to replace any non-digit character by the character "-".

### 208: extracting delimited data from one line

Given the string "fld1_,fld2__,fld3,,__fld4_,_fld5", use the `re` module to extract the data, so that the result is the following list: ["fld1", "fld2", "fld3", "fld4", "fld5"].

### 209: extracting data from multiple lines

Suppose that we have the following text that contains multiple valid records, along with invalid records with random data, mimicking what you'd get out of a DB log after a crash:

```
101, Homework; Complete physics and math
some random nonsense
102, Laundry; Wash all the clothes today
54, random; record
103, Museum; All about Egypt
1234, random; record
Another random record
```

1. Write a regex pattern that identifies the valid records and tells them apart from the invalid ones.
2. Use that regex pattern to create a snippet that prints the matched and non-matched records. For the matched ones, the individual fields task id, task title, and task description must be identified (HINT: use groups). The report should be correctly formatted as shown below:
    ```
    Matched:  task_id='task_id', task_title='task_title', task description='task_description'
    No Match: <invalid record>
    ```
3. Enhance the previous snippet so that you return a list of Task NamedTuples.

### 210: hello, named groups

Textual information provides more semantics than raw regular expressions.

Python supports the syntax:

```python
?P<group_name>pattern
```

to give a name to a pattern group.

When doing so, you will be able to use `match.group(<group_name>)` instead of its index, which will improve your code's readability.

Suppose that we have the following text that contains multiple valid records, along with invalid records with random data, mimicking what you'd get out of a DB log after a crash:

```
101, Homework; Complete physics and math
some random nonsense
102, Laundry; Wash all the clothes today
54, random; record
103, Museum; All about Egypt
1234, random; record
Another random record
```

1. Write a regex pattern that identifies the valid records and tells them apart from the invalid ones using named groups.
2. Use that regex pattern to create a snippet that prints the matched and non-matched records. For the matched ones, the individual fields task id, task title, and task description must be identified (HINT: use named groups). The report should be correctly formatted as shown below:
    ```
    Matched:  task_id, task_title, task description
    No Match: <invalid record>
    ```
3. Enhance the previous snippet so that you return a list of Task NamedTuples, leveraging named groups.

### 211: using groupdict with regular expressions with group names

The `groupdict()` method allows you to create a dictionary with the named groups.

Suppose that we have the following text that contains multiple valid records, along with invalid records with random data, mimicking what you'd get out of a DB log after a crash:

```
101, Homework; Complete physics and math
some random nonsense
102, Laundry; Wash all the clothes today
54, random; record
103, Museum; All about Egypt
1234, random; record
Another random record
```

1. Write a regex pattern that identifies the valid records and tells them apart from the invalid ones using named groups.
2. Use that regex pattern to create a snippet that prints the matched and non-matched records. For the matched ones, the individual fields task id, task title, and task description must be identified (HINT: use named groups). The report should be correctly formatted as shown below:
    ```
    Matched:  task_id, task_title, task description
    No Match: <invalid record>
    ```
3. Enhance the previous snippet so that you return a list of dicts, leveraging named groups and `groupdict()`.

4. Enhance the previous snippet to create corresponding `Task` instances as NamedTuples.

### 212: lists vs. tuples

