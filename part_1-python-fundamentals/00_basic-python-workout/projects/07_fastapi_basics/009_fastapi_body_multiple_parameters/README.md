# 009: Using multiple body parameters with FastAPI
> Illustrates how to use multiple body parameters

## Project description

FastAPI lets you mix `Path`, `Query`, and multiple body parameters in your path operations.

### Mixing `Path`, query parameters, and body parameters

Create a path operation for `PUT /items/{item_id}` including:
+ An optional request body model for an Item with fields:
  + name: required string
  + description: optional string
  + price: required float
  + tax: optional float
+ an int path parameter `item_id` with title "Item ID" whose value must be between 0 and 1000 (inc.).
+ `q` an optional query parameter

In the path operation, return a dictionary with the elements received.

Validate that the body parameter is optional.

### Multiple body parameters

Create a path operation for `POST /items/{item_id}` that accepts:
+ a path parameter `item_id`
+ a request body parameter `item` with the fields:
  + name: required string
  + description: optional string
  + price: required float
  + tax: optional float
  + tags: an optional list of strings
+ a request body parameter `user` with the fields:
  + username: required string
  + full_name: optional string

In the path operation, return the information received. What's the shape of the expected request body?

SOLUTION:

The shape of the request body when you use multiple body parameters is the following:

```json
{
    "item": {
        "description": "foobar",
        "name": "foo",
        "price": 1.23,
        "tags": [
            "baz",
            "foobar"
        ],
        "tax": 3.21
    },
    "item_id": 1,
    "user": {
        "full_name": "Jason Isaacs",
        "username": "jason"
    }
}
```


You can test it with HTTPie using:

```bash
$ http post :5000/items/1 user[username]="jason" user[full_name]="Jason Isaacs" item[name]="foo" item[description]="bar" item[price]=1.23 item[tax]=3.21 item[tags][]="baz" item[tags][]="foobar"
```

Note the special syntax for `item.tags`.

Alternatively, you can use raw JSON (why do you need to learn a new syntax?):

```bash
$ http post :5000/items/1 --raw '{"user":{"username": "jason", "full_name":"Jason Isaacs"},"item":{"name":"foo", "description":"foobar", "price":1.23, "tax":3.21, "tags":["baz", "foobar"]}}
```



### Adding a singular value in the body

Create a path operation for `POST /v2/items/{item_id}` that accepts:
+ a path parameter `item_id`
+ a request body parameter `item` with the fields:
  + name: required string
  + description: optional string
  + price: required float
  + tax: optional float
  + tags: optional list of strings
+ a request body parameter `user` with the fields:
  + username: required string
  + full_name: optional string
+ a singular value `importance` which is a required int.

In the path operation, return the information received. What's the shape of the expected request body?

SOLUTION:

The shape of the JSON body is:

```json
{
    "importance": 5,
    "item": {
        "description": "bar",
        "name": "foo",
        "price": 1.23,
        "tags": [
            "baz",
            "foobar"
        ],
        "tax": 3.21
    },
    "item_id": 1,
    "user": {
        "full_name": "Jason Isaacs",
        "username": "jason"
    }
}
```

And you can test it with:

```bash
$ http post
:5000/v2/items/1 user[username]="jason" user[full_name]="Jason Isaacs" item[name]="foo" item[description]="bar" item[price]=1.23 item[tax]=3.21 item[tags][]="baz" item[tags][]="foobar" importance=5
```

### Multiple body and query parameters

Create a path operation for `POST /v3/items/{item_id}` that accepts:
+ a path parameter `item_id`
+ a request body parameter `item` with the fields:
  + name: required string
  + description: optional string
  + price: required float
  + tax: optional float
  + tags: an optional list of strings
+ a request body parameter `user` with the fields:
  + username: required string
  + full_name: optional string
+ a singular value `importance` which is a required int.
+ an optional string query parameter `q`

In the path operation, return the information received.

SOLUTION:

You can test it with:

```bash
$ http post :5000/v3/items/1 user[username]="jason" user[full_name]="Jason Isaacs" item[name]="foo" item[description]="bar" item[price]=1.23 item[tax]=3.21 item[tags][]="baz" item[tags][]="foobar" importance=5 q==query-string
```


### Embedding body parameters

Create a path operation for `POST /v4/items/{item_id}` that accepts:
+ a path parameter `item_id`
+ a request body parameter `item` with the fields:
  + name: required string
  + description: optional string
  + price: required float
  + tax: optional float

in which the request body parameter is embedded in a `"item"` key. That is, the path operation should accept the following JSON as the body payload:

```json
{
    "item": {
        "name": "Foo",
        "description": "Bar",
        "price": 42.0,
        "tax": 3.2
    }
}
```


In the path operation, return the information received.


## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

The only other dependency was ruff:

```bash
$ uv add ruff --dev
```
