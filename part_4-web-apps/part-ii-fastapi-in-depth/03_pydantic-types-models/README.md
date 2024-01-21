# Pydantic, Type Hints, and Models

FastAPI stands largely on a Python package called Pydantic. This uses *models* (i.e., Python object classes) to define data structures.

When using FastAPI, you define how data should be using canonical Python, and Pydantic will take charge of the validations.

## Type Hinting

In Python, variables are just names associated with objects, and it's the objects that have types.

Because Python is special in that way, and many programming errors can be avoided by adding types to variables, Python introduced type hints in the standard typing module.

The Python interpreter ignores the type hint and runs the program as though there were not type hints, but tools and frameworks can use this information to warn you about mismatches.

Pydantic uses that to perform validations, and its integration with FastAPI makes a lot of web development issues much easier to handle.

The following are examples of type hints:

```python
from typing import Any

some_tuple: tuple = "uno", "dos", "tres", "catorce"
some_dict: dict = {"Marco": "Polo", "age": 49}
some_dict: dict[str, Any] = {"Marco": "Polo", "age": 49}
some_dict: dict[str, str | int] = {"Marco": "Polo", "age": 49}
```

## Data Grouping with dataclasses

The `@dataclass` decorator available in the `dataclasses` module lets you eliminate the boilerplate associated with the creation of classes that hold values. That is, a dataclass is very similar to the `struct` concept available in other programming languages.

Compared with named tuples, data classes support mutability, can be enriched with custom methods, and support inheritance.

A dataclass representing a restaurant bill will look like the following:

```python
from dataclasses import dataclass

@dataclass
class Bill:
  table_number: int
  meal_amount: float
  served_by: str
  tip_amount: float
```

Consider a more contrived example involving imaginary creatures (*cryptids*) and explorers who seek them.

The cryptid initial definition might look like the following:
+ name: Key, string.
+ country: Two-character ISO country code, or `"*"` for all.
+ area: Optional, string, state or other country subdivision.
+ description: freeform, string.
+ aka: also known as, freeform, string.


Explorers will be defined as:
+ name: Key, string.
+ country: Two-character ISO country code, or `"*"` for all.
+ description: freeform, string.

Using a dataclass we could define:

```python
from dataclasses import dataclass

@dataclass
class CreatureDataClass():
  name: str
  country: str
  area: str
  description: str
  aka: str
```

And we could define instances using the following syntax:

```python
yeti = CreatureDataClass(
  "yeti",
  "CN",
  "Himalayas",
  "Hirsute Himalayan",
  "Abominable Snowman",
)
```

And we can access the dataclass instance properties as regular object properties:

```python
print(f"Name is {yeti.name}")
```

## Alternatives

Pydantic is a third party alternative to dataclasses. Because it is integrated with FastAPI and can be used for validation (one of the major concerns of web APIs) we will end up using Pydantic as an alternative to standard Python dataclasses.

Additionally, Pydantic uses standard Python type hint syntax.

At a high-level, Pydantic provide ways to specify a combination of the following checks:
+ Required vs. Optional
+ Default value if unspecified but required
+ Data type or types expected
+ Value range restrictions
+ Custom function-based checks support
+ Serialization and deserialization

## Validating types and values

Pydantic uses the model/schema definitions to validate the types.

The following table lists some restrictions/actions that can be placed on the values:

| Type it applies to | Restriction | Description |
| :----------------- | :---------- | :---------- |
| Integer (`conint`) or `float` | `gt` | Greater than. |
| Integer (`conint`) or `float` | `lt` | Less than. |
| Integer (`conint`) or `float` | `ge` | Greater than or equal to. |
| Integer (`conint`) or `float` | `lt` | Less than  or equal to. |
| Integer (`conint`) or `float` | `multiple_of` | Integer multiple of given value. |
| String (`constr`) | `min_length` | Minimum character (not byte) length. |
| String (`constr`) | `max_length` | Maximum character (not byte) length. |
| String (`constr`) | `to_upper` | Convert to uppercase (action). |
| String (`constr`) | `to_lower` | Convert to lowercase (action). |
| String (`constr`) | `regex` | Match a Python regular expression. |
| Tuple, list, or set | `min_items` | Minimum number of elements. |
| Tuple, list, or set | `max_items` | Maximum number of elements. |

This snippet illustrates how you specify these restrictions/actions using a `constr` which is a *constrained string* in Pydantic terms.

```python
from pydantic import BaseModel, constr

class Creature(BaseModel):
    name: constr(min_length=1, to_upper=True) # type: ignore
    country: str
    area: str
    description: str
    aka: str
```

Alternatively, you can do the same using `Field`:

```python
from pydantic import BaseModel, constr, Field


class Creature(BaseModel):
    name: constr(min_length=1, to_upper=True) # type: ignore
    country: str
    area: str
    description: str = Field(..., min_length=2)
    aka: str
```


## Review