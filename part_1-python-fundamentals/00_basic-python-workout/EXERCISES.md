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

Create another snippet that uses `and` expression between two variables `x` and `y` and check what happens when you assign values such as `True` and `False`, `1` and `0`, `"some"` and `""`.

### 142: is operator

`is` is the identity operator, returning `True` if and only if two objects are the same object.

1. Create two strings with values `"hello"` and `"hello"`. Compare them with `==` and `is`.

2. Create two numbers with values `5` and `5`. Compare them with `==` and `is`.

3. Create a boolean variable `True`. Compare it with `True` using `==` and `is`.

4. Create a simple `Person` class and implement `__eq__`. Create two identical instances of the `Person` class (e.g., `Person("Jason", 53)`) and compare them with `is` and `==`.

### 143: in operator

`in` is the membership operator, returning `True` if a value is contained in a sequence.

1. Create a list and use the `in` operator to check if a given value is in the list.
2. Create a dictionary and use the `in` operator to check if a given key-value pair is in the list (if possible)

### 144: the ternary operator

The syntax for the ternary operator in Python is:

```python
result_if_true if condition else result_if_false
```

Use the ternary operator to create an expression that returns `True` when passed a number over 18 and wrap it in a function called `is_adult`. Can you use an `and` expression to obtain the same result?

## 15: More on strings
