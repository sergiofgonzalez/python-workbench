# 011: FastAPI: nested models for request bodies
> Illustrates the basics of nested models for request bodies in FastAPI

## Project description

FastAPI supports arbitrarily nested models for your request bodies.

### Typed list fields

Define a path operation for `PUT /items/{item_id}` which expects an Item body parameter with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: optional float
+ tags: list of strings, with empty list being the default

SOLUTION:

This can be tested with

```bash
$ http put :5000/items/1 name="foo" price=2.31 tags[]="foo" tags[]="bar" tags[]="baz"
```

### Typed set fields

Define a path operation for `PUT /v2/items/{item_id}` which expects an Item body parameter with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: optional float
+ tags: set of strings, with empty set being the default

Ensure that when you send duplicated tags in the payload, the duplicates are automatically discarded.

### Nested models

Define a path operation for `PUT /v3/items/{item_id}` which expects an Item body parameter with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: optional float
+ tags: set of strings, with empty set being the default
+ image: an Image model containing in turn the fields:
  + url: required HttpUrl type
  + name: required string

Confirm that you cannot send a random string in the url field.

HINT: HttpUrl is a Pydantic field type.

SOLUTION:

This can be tested with:

```bash
$ http put :5000/v3/items/1 name="foo" price=2.31 tags[]="foo" tags[]="bar" tags[]="baz" tags[]="foo" image[url]=http://example.com/pic.png image[name]="foobar"
```

### Attributes with a list of submodels

Define a path operation for `PUT /v3/items/{item_id}` which expects an Item body parameter with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: optional float
+ tags: set of strings, with empty set being the default
+ image: list of Image models containing in turn the fields:
  + url: required HttpUrl type
  + name: required string

Confirm that you cannot send random strings in the url field.

SOLUTION:

This can be tested with:

```bash
$ http put :5000/v4/items/1 name="foo" price=2.31 tags[]="foo" tags[]="bar" tags[]="baz" tags[]="foo" images[0][url]=http://example.com/pic1.png images[0][name]="foobar1" images[1][url]=http://example.com/pic2.png images[1][name]="foobar2"
```

### Deeply nested models

Define a path operation for `POST /offers/` which expects an Offer body parameter with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ items: required list of items, containing:
    + name: required string
    + description: optional string
    + price: required float
    + tax: optional float
    + tags: set of strings, with empty set being the default
    + image: list of Image models containing in turn the fields:
      + url: required HttpUrl type
      + name: required string

Confirm that you cannot send a random string in the url field.

This can be tested with:

```bash
$ http post :5000/offers/ name="offer_name" description="offer_description" price=12345.67 items[0][name]="item0" items[0][price]=1.11 items[0][images][0][url]=http://example.com/pic1.png items[0][images][0][name]="pic1"
```

### Bodies of pure lists

Create a path operation for `POST /images/multiple/` that must accept a list of images, where the list (JSON array) is the top most element.

That is:

```json
[
    {
        "name": "pic1",
        "url": "http://example.com/pic1.png"
    },
    {
        "name": "pic2",
        "url": "http://example.com/pic2.png"
    }
]
```

The Image object is defined as:
+ url: required HttpUrl type
+ name: required string

SOLUTION:

This can be tested with:

```bash
$ http post :5000/images/multiple/ [0][url]=http://example.com/pic1.png [0][name]="pic1" [1][url]=http://example.com/pic2.png [1][name]="pic2"
```

### Bodies of arbitrary dicts

Create a path operation for `POST /index-weights/` which accepts a weights body parameter which accepts an arbitrary dict where the keys are ints and the values are floats.

SOLUTION:

This can be tested with:

```bash
$ http post :5000/index-weights/ 1=1.1 2=2.22
```

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
